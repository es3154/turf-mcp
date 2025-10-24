# 工具包

import asyncio


async def call_js_script(js_script: str) -> str:
    """使用node执行js脚本"""
    try:
        # 使用 asyncio.create_subprocess_exec 异步执行命令
        process = await asyncio.create_subprocess_exec(
            'node', '-e', js_script,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # 等待结果，设置超时
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=10)
        
        # 解码输出
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')

        # 检查是否有错误
        if process.returncode != 0:
            raise Exception(f"Node.js执行失败: {stderr}")

        if stderr:
            print(f"JavaScript警告或错误: {stderr}")

        return stdout.strip()

    except asyncio.TimeoutError:
        raise Exception("JavaScript执行超时")
    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")



async def main():
    s = "console.log(111)"
    result = await call_js_script(s)
    print(result)


if __name__ == '__main__':
    asyncio.run(main())

