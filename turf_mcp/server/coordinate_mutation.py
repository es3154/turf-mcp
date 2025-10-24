# 坐标转换函数

from fastmcp import FastMCP

from turf_mcp.utils import call_js_script

coordinate_mutation_mcp = FastMCP("coordinate_mutation")

@coordinate_mutation_mcp.tool
async def clean_coords(geojson: str, options: str = None) -> str:
    """
    清理 GeoJSON 数据中的冗余坐标点。
    
    此功能自动移除连续的重复坐标点，简化几何图形，使数据更加整洁。
    
    Args:
        geojson: GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[0, 0], [0, 2], [0, 5], [0, 8], [0, 8], [0, 10]]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - mutate: 是否允许修改输入 GeoJSON (默认: false)
            - 示例: '{"mutate": true}'
    
    Returns:
        str: JSON 字符串格式的清理后的 GeoJSON 特征或几何图形
            - 类型: 与输入相同的 GeoJSON 类型
            - 格式: 清理冗余坐标后的 GeoJSON
            - 示例: '{"type": "LineString", "coordinates": [[0, 0], [0, 10]]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> line = '{"type": "LineString", "coordinates": [[0, 0], [0, 2], [0, 5], [0, 8], [0, 8], [0, 10]]}'
        >>> result = asyncio.run(clean_coords(line))
        >>> print(result)
        '{"type": "LineString", "coordinates": [[0, 0], [0, 10]]}'
    
    Notes:
        - 输入参数 geojson 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 会移除连续的重复坐标点
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const options = JSON.parse('{options_param}');
        const result = turf.cleanCoords(geojson, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@coordinate_mutation_mcp.tool
async def flip(geojson: str, options: str = None) -> str:
    """
    交换坐标的经度和纬度位置。
    
    此功能将坐标从 [经度, 纬度] 格式转换为 [纬度, 经度] 格式，适用于不同系统的坐标约定。
    
    Args:
        geojson: GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [20.566406, 43.421008]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - mutate: 是否允许修改输入 GeoJSON (默认: false)
            - 示例: '{"mutate": true}'
    
    Returns:
        str: JSON 字符串格式的坐标翻转后的 GeoJSON 特征
            - 类型: GeoJSON Feature
            - 格式: 坐标翻转后的 GeoJSON
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [43.421008, 20.566406]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> point = '{"type": "Point", "coordinates": [20.566406, 43.421008]}'
        >>> result = asyncio.run(flip(point))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [43.421008, 20.566406]}}'
    
    Notes:
        - 输入参数 geojson 和 options 必须是有效的 JSON 字符串
        - 坐标顺序从 [经度, 纬度] 翻转为 [纬度, 经度]
        - 主要用于在不同坐标系约定之间转换
        - 依赖于 Turf.js 库和 Node.js 环境
        - 注意：输入如果是几何图形，输出会转换为特征对象
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const options = JSON.parse('{options_param}');
        const result = turf.flip(geojson, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@coordinate_mutation_mcp.tool
async def rewind(geojson: str, options: str = None) -> str:
    """
    修正多边形的环方向，确保外环逆时针、内环顺时针。
    
    此功能自动调整多边形的环方向，符合地理信息系统标准，确保多边形区域计算正确。
    
    Args:
        geojson: GeoJSON 多边形特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Polygon 或 MultiPolygon 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Polygon", "coordinates": [[[121, -29], [138, -29], [138, -18], [121, -18], [121, -29]]]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - reverse: 是否启用反向重绕 (默认: false)
                - mutate: 是否允许修改输入 GeoJSON (默认: false)
            - 示例: '{"reverse": true, "mutate": false}'
    
    Returns:
        str: JSON 字符串格式的重绕后的 GeoJSON 多边形
            - 类型: GeoJSON Feature with Polygon geometry
            - 格式: 重绕环方向后的多边形
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[121, -29], [121, -18], [138, -18], [138, -29], [121, -29]]]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> polygon = '{"type": "Polygon", "coordinates": [[[121, -29], [138, -29], [138, -18], [121, -18], [121, -29]]]}'
        >>> result = asyncio.run(rewind(polygon))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[121, -29], [121, -18], [138, -18], [138, -29], [121, -29]]]}}'
    
    Notes:
        - 输入参数 geojson 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 外环应为逆时针方向，内环应为顺时针方向
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const options = JSON.parse('{options_param}');
        const result = turf.rewind(geojson, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@coordinate_mutation_mcp.tool
async def round_number(num: float, precision: int = 0) -> str:
    """
    对数字进行四舍五入，控制小数位数。
    
    此功能将数字四舍五入到指定的小数位数，用于精确控制数值的精度。
    
    Args:
        num: 要四舍五入的数字
            - 类型: float
            - 范围: 任意浮点数
            - 示例: 120.4321
        
        precision: 小数位数精度
            - 类型: int
            - 描述: 要保留的小数位数
            - 默认: 0
            - 范围: 0 或正整数
            - 示例: 2
    
    Returns:
        str: JSON 字符串格式的四舍五入结果对象
            - 类型: 包含 value 的对象
            - 格式: {"value": 四舍五入后的数值}
            - 示例: '{"value": 120.43}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> result = asyncio.run(round_number(120.4321, 2))
        >>> print(result)
        '{"value": 120.43}'
    
    Notes:
        - 如果未提供精度参数，默认四舍五入到整数
        - 精度为 0 时返回整数
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const num = {num};
        const precision = {precision};
        const result = turf.round(num, precision);
        console.log(JSON.stringify({{"value": result}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@coordinate_mutation_mcp.tool
async def truncate(geojson: str, options: str = None) -> str:
    """
    截断 GeoJSON 几何图形的坐标精度。
    
    该函数使用 Turf.js 库的 truncate 方法，减少 GeoJSON 几何图形坐标的小数精度，
    并可选择移除 Z 坐标值。
    
    Args:
        geojson: GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [70.46923055566859, 58.11088890802906, 1508]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - precision: 坐标小数精度 (默认: 6)
                - coordinates: 最大坐标维度数 (主要用于移除 Z 坐标) (默认: 3)
                - mutate: 是否允许修改输入 GeoJSON (默认: false)
            - 示例: '{"precision": 3, "coordinates": 2, "mutate": false}'
    
    Returns:
        str: JSON 字符串格式的精度截断后的 GeoJSON 特征
            - 类型: GeoJSON Feature
            - 格式: 坐标精度截断后的 GeoJSON
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [70.469, 58.111]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> point = '{"type": "Point", "coordinates": [70.46923055566859, 58.11088890802906, 1508]}'
        >>> options = '{"precision": 3, "coordinates": 2}'
        >>> result = asyncio.run(truncate(point, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [70.469, 58.111]}}'
    
    Notes:
        - 输入参数 geojson 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 通过设置 coordinates 为 2 可以移除 Z 坐标值
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const options = JSON.parse('{options_param}');
        const result = turf.truncate(geojson, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")
