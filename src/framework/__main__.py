from .fastapi import FastAPIFramework


def get_web_framework(framework_name: str) -> Any:
    framework_map = {
        "fastapi": FastAPIFramework,
        # 在这里可以添加其他框架的映射
    }
    framework_class = framework_map.get(framework_name.lower())
    if not framework_class:
        raise ValueError(f"Unsupported web framework: {framework_name}")
    framework = framework_class()
    if isinstance(framework, FastAPIFramework):
        framework.find_and_register_app()
    return framework