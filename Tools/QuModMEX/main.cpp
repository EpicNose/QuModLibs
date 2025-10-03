#include <iostream>
#include "utils/EnvEncode.h"
#include "QuModMEX.h"
// By Zero123

// 列表转字符串
static std::string listToString(const std::vector<std::string>& vc)
{
	std::string result = "[";
	for (const auto& str : vc)
	{
		result.append(str+", ");
	}
	if(result.size() >= 2)
	{
		result.erase(result.end() - 2, result.end());
	}
	result.append("]");
	return result;
}

// set转字符串
static std::string listToString(const std::unordered_set<std::string>& vc)
{
	// set转vector
	std::vector<std::string> vec(vc.begin(), vc.end());
	return listToString(vec);
}

// 按空格化分字符串参数
static std::vector<std::string> splitString(const std::string& str)
{
	std::vector<std::string> result;
	std::istringstream iss(str);
	std::string token;
	while (iss >> token)
	{
		result.push_back(token);
	}
	return result;
}

// 刷新输入缓冲区
static void flushCin()
{
	std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

static std::string readLine(std::istream& in = std::cin)
{
	std::string line;
	std::getline(std::cin, line);
	return line;
}

// 获取用户输入的参数
static std::vector<std::string> getUserInputArgs()
{
	return splitString(readLine());
}

// 删除空Python目录
static void removeNullPythonDirs(const std::filesystem::path& path)
{
	if(!std::filesystem::is_directory(path))
	{
		return;
	}
	unsigned int count = 0;
	for (const auto& entry : std::filesystem::directory_iterator(path))
	{
		// 忽略 __init__.py 文件
		if (std::filesystem::is_regular_file(entry) && entry.path().filename() != "__init__.py")
		{
			count++;
		}
		else if (std::filesystem::is_directory(entry))
		{
			count++;
		}
	}
	if (count == 0)
	{
		std::cout << "删除空目录: " << path.generic_string() << "\n";
		std::filesystem::remove_all(path);
		return;
	}
}

// 白名单处理模式
static void whiteMode(const std::filesystem::path& quModPath)
{
	auto analyzer = QuModMEX::QuModLibsAnalyzer(quModPath);
	auto manager = QuModMEX::ModuleRelationViewManager{ analyzer.getAllModulesRelationViews() };
	std::unordered_set<std::string> targets;
	std::cout << "请输入需要保留的白名单模块(空格分隔): ";
	auto userArgs = getUserInputArgs();
	std::cout << "\n";
	targets = std::unordered_set<std::string>(userArgs.begin(), userArgs.end());
	std::cout << "保留目标: " << listToString(targets) << "\n";
	auto canRemove = manager.getRemoveUnwantedModules(targets);
	std::cout << "根据分析，可安全移除（按下回车执行）: " << listToString(canRemove) << "\n";
	system("pause");
	auto mPath = quModPath / "Modules";
	for (const auto& m : canRemove)
	{
		auto path = mPath / m;
		if (std::filesystem::exists(path))
		{
			std::cout << "删除模块: " << path.generic_string() << "\n";
			std::filesystem::remove_all(path);
		}
		else
		{
			std::cout << "模块不存在: " << path.generic_string() << "\n";
		}
	}
	removeNullPythonDirs(mPath);
}

// 黑名单处理模式
static void blackMode(const std::filesystem::path& quModPath)
{
	auto analyzer = QuModMEX::QuModLibsAnalyzer(quModPath);
	auto mRv = analyzer.getAllModulesRelationViews();
	auto manager = QuModMEX::ModuleRelationViewManager{ mRv };
	std::unordered_set<std::string> targets;
	std::cout << "请输入需要剔除的黑名单模块(空格分隔): ";
	auto userArgs = getUserInputArgs();
	targets = std::unordered_set<std::string>(userArgs.begin(), userArgs.end());
	std::cout << "移除目标: " << listToString(targets) << "\n";
	// 反向白名单生成
	std::unordered_set<std::string> targets2;
	for (const auto& [name, _] : manager.getViewDatas())
	{
		if(targets.find(name) == targets.end())
		{
			targets2.insert(name);
		}
	}
	auto canRemove = manager.getRemoveUnwantedModules(targets2);
	if (canRemove.empty())
	{
		std::cout << "\n根据分析，没有相关可安全移除的模块。\n";
		for (auto& view : mRv)
		{
			if (targets.find(view.getName()) != targets.end())
			{
				std::cout << view.getName() << " 被" << view.getRefedCount() << "个模块引用。\n";
				std::cout << "以下模块依赖: " << listToString(view.getRefedModules()) << "\n";
				std::cout << "\n";
			}
		}
		return;
	}
	std::cout << "根据分析，可安全移除（按下回车执行）: " << listToString(canRemove) << "\n";
	system("pause");
	auto mPath = quModPath / "Modules";
	for (const auto& m : canRemove)
	{
		auto path = mPath / m;
		if (std::filesystem::exists(path))
		{
			std::cout << "删除模块: " << path.generic_string() << "\n";
			std::filesystem::remove_all(path);
		}
		else
		{
			std::cout << "模块不存在: " << path.generic_string() << "\n";
		}
	}
	removeNullPythonDirs(mPath);
}

// 仅计算依赖关系
static void onlyListMode(const std::filesystem::path& quModPath)
{
	auto analyzer = QuModMEX::QuModLibsAnalyzer(quModPath);
	auto relationViews = analyzer.getAllModulesRelationViews();
	for (auto& view : relationViews)
	{
		std::cout << view.getName() << " 共引用" << view.getRefCount() << "个模块，被" << view.getRefedCount() << "个模块引用。\n";
		std::cout << "引用: " << listToString(view.getRefModules()) << "\n";
		std::cout << "被引用: " << listToString(view.getRefedModules()) << "\n";
		std::cout << "\n";
	}
}

int main()
{
	Encoding::initEnvcode();
	std::cout << R"(---------------------------------------------------
QuModMEX使用说明：
- 该项目用于分析依赖并剔除无用QuModLibs模块
- 提供两种剔除模式:
  0. 白名单模式，保留特定模块及其依赖
  1. 黑名单模式，移除特定模块（依赖检查）
  2. 仅列出依赖关系，不作其他处理
- 若需要移除补全库，另见：QuModPurge.exe
- 特殊: Include扩展无互相依赖关系，若无需求可直接删除
---------------------------------------------------
)";
	std::filesystem::path targetPath;
	std::cout << "\n请输入目标路径(QuModLibs): ";
	targetPath = readLine();
	std::cout << "目标路径：" << targetPath << "\n\n";
	if (!std::filesystem::exists(targetPath / "QuMod.py"))
	{
		std::cout << "目标路径不存在QuMod.py文件，请检查路径是否正确。\n";
		system("pause");
		return 0;
	}
	std::cout << "请输入处理策略(0/1/2): ";
	std::vector<std::string> modeArgs = getUserInputArgs();
	std::cout << "\n";
	if (modeArgs.size() != 1)
	{
		std::cout << "输入参数错误，请检查输入格式。\n";
		system("pause");
		return 0;
	}
	if (modeArgs[0] == "0")
	{
		whiteMode(targetPath);
	}
	else if (modeArgs[0] == "1")
	{
		blackMode(targetPath);
	}
	else if (modeArgs[0] == "2")
	{
		onlyListMode(targetPath);
	}
	else
	{
		std::cout << "不支持的策略模式：" << modeArgs[0] << "\n";
	}
	system("pause");
	return 0;
}