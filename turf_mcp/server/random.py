# 随机地理数据生成函数

from fastmcp import FastMCP

from turf_mcp.utils import call_js_script

random_mcp = FastMCP("random")

@random_mcp.tool
async def randomPosition(bbox: str = None) -> str:
    """
    生成随机的地理坐标位置。
    
    此功能在指定的边界框内随机生成一个地理坐标位置，返回经度和纬度坐标。
    
    Args:
        bbox: 边界框数组
            - 类型: str (JSON 字符串格式的数组) 或 None
            - 格式: [minX, minY, maxX, maxY]
            - 默认: [-180, -90, 180, 90] (全球范围)
            - 示例: '[-180, -90, 180, 90]'
    
    Returns:
        str: JSON 字符串格式的坐标位置数组
            - 类型: 数组 [经度, 纬度]
            - 格式: [lng, lat]
            - 示例: '[-75.343, 39.984]'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> bbox = '[-180, -90, 180, 90]'
        >>> result = asyncio.run(randomPosition(bbox))
        >>> print(result)
        '[-75.343, 39.984]'
    
    Notes:
        - 输入参数 bbox 必须是有效的 JSON 字符串或 None
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 如果未指定边界框，默认在全球范围内生成随机位置
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    bbox_param = bbox if bbox else '[-180, -90, 180, 90]'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const bbox = JSON.parse('{bbox_param}');
        const result = turf.randomPosition(bbox);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@random_mcp.tool
async def randomPoint(count: int = 1, options: str = None) -> str:
    """
    生成随机点特征集合。
    
    此功能在指定边界框内生成指定数量的随机点，返回点特征集合。
    
    Args:
        count: 生成点的数量
            - 类型: int
            - 默认: 1
            - 示例: 25
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - bbox: 边界框数组 [minX, minY, maxX, maxY] (默认: [-180, -90, 180, 90])
            - 示例: '{"bbox": [-180, -90, 180, 90]}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Point features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}}, ...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> result = asyncio.run(randomPoint(25))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, ...]}'
    
    Notes:
        - 输入参数 options 必须是有效的 JSON 字符串或 None
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 如果未指定边界框，默认在全球范围内生成随机点
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const count = parseInt({count});
        const options = JSON.parse('{options_param}');
        const result = turf.randomPoint(count, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@random_mcp.tool
async def randomLineString(count: int = 1, options: str = None) -> str:
    """
    生成随机线特征集合。
    
    此功能在指定边界框内生成指定数量的随机线，返回线特征集合。
    
    Args:
        count: 生成线的数量
            - 类型: int
            - 默认: 1
            - 示例: 25
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - bbox: 边界框数组 [minX, minY, maxX, maxY] (默认: [-180, -90, 180, 90])
                - num_vertices: 每条线的顶点数量 (默认: 10)
                - max_length: 顶点与前一个顶点的最大距离 (默认: 0.0001)
                - max_rotation: 线段与前一线段的最大旋转角度 (默认: Math.PI/8)
            - 示例: '{"bbox": [-180, -90, 180, 90], "num_vertices": 10}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with LineString features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}}, ...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-74, 40], [-78, 42], [-82, 35]]}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> result = asyncio.run(randomLineString(25))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-74, 40], [-78, 42], [-82, 35]]}}, ...]}'
    
    Notes:
        - 输入参数 options 必须是有效的 JSON 字符串或 None
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 如果未指定边界框，默认在全球范围内生成随机线
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const count = parseInt({count});
        const options = JSON.parse('{options_param}');
        const result = turf.randomLineString(count, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@random_mcp.tool
async def randomPolygon(count: int = 1, options: str = None) -> str:
    """
    生成随机多边形特征集合。
    
    此功能在指定边界框内生成指定数量的随机多边形，返回多边形特征集合。
    
    Args:
        count: 生成多边形的数量
            - 类型: int
            - 默认: 1
            - 示例: 25
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - bbox: 边界框数组 [minX, minY, maxX, maxY] (默认: [-180, -90, 180, 90])
                - num_vertices: 每个多边形的顶点数量 (默认: 10)
                - max_radial_length: 顶点距离多边形中心的最大径向长度 (默认: 10)
            - 示例: '{"bbox": [-180, -90, 180, 90], "num_vertices": 10}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Polygon features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}, ...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[125, -15], [113, -22], [154, -27], [144, -15], [125, -15]]]}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> result = asyncio.run(randomPolygon(25))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[125, -15], [113, -22], [154, -27], [144, -15], [125, -15]]]}}, ...]}'
    
    Notes:
        - 输入参数 options 必须是有效的 JSON 字符串或 None
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 如果未指定边界框，默认在全球范围内生成随机多边形
        - 多边形会自动闭合，首尾坐标点相同
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const count = parseInt({count});
        const options = JSON.parse('{options_param}');
        const result = turf.randomPolygon(count, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")
