# 特征转换函数

from fastmcp import FastMCP

from turf_mcp.utils import call_js_script

feature_conversion_mcp = FastMCP("feature_conversion")

@feature_conversion_mcp.tool
async def combine(feature_collection: str) -> str:
    """
    将特征集合合并为复合几何图形。
    
    此功能将点、线或多边形特征集合分别合并为多点、多线或多边形复合几何图形。
    
    Args:
        feature_collection: GeoJSON 特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON FeatureCollection 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [19.026432, 47.49134]}}, {"type": "Feature", "geometry": {"type": "Point", "coordinates": [19.074497, 47.509548]}}]}'
    
    Returns:
        str: JSON 字符串格式的合并后 GeoJSON 特征集合
            - 类型: GeoJSON FeatureCollection with MultiPoint, MultiLineString or MultiPolygon features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "...", "coordinates": [...]}}]}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> fc = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [19.026432, 47.49134]}}, {"type": "Feature", "geometry": {"type": "Point", "coordinates": [19.074497, 47.509548]}}]}'
        >>> result = asyncio.run(combine(fc))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "MultiPoint", "coordinates": [[19.026432, 47.49134], [19.074497, 47.509548]]}}]}'
    
    Notes:
        - 输入参数 feature_collection 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 点特征会合并为多点，线特征会合并为多线，多边形特征会合并为多多边形
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const featureCollection = JSON.parse('{feature_collection}');
        const result = turf.combine(featureCollection);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@feature_conversion_mcp.tool
async def explode(geojson: str) -> str:
    """
    将几何图形分解为单独的点特征。
    
    此功能将给定的 GeoJSON 特征分解为所有顶点坐标的单独点特征集合。
    
    Args:
        geojson: GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Polygon", "coordinates": [[[-81, 41], [-88, 36], [-84, 31], [-80, 33], [-77, 39], [-81, 41]]]}'
    
    Returns:
        str: JSON 字符串格式的点特征集合
            - 类型: GeoJSON FeatureCollection with Point features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}}, ...]}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> polygon = '{"type": "Polygon", "coordinates": [[[-81, 41], [-88, 36], [-84, 31], [-80, 33], [-77, 39], [-81, 41]]]}'
        >>> result = asyncio.run(explode(polygon))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-81, 41]}}, ...]}'
    
    Notes:
        - 输入参数 geojson 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 返回所有几何图形顶点的点特征集合
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const result = turf.explode(geojson);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@feature_conversion_mcp.tool
async def flatten(geojson: str) -> str:
    """
    将复合几何图形展平为简单几何图形。
    
    此功能将多几何图形（如多点、多线、多多边形）展平为对应的简单几何图形特征集合。
    
    Args:
        geojson: GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "MultiPolygon", "coordinates": [[[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]], [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]]]}'
    
    Returns:
        str: JSON 字符串格式的展平后特征集合
            - 类型: GeoJSON FeatureCollection with simple geometry features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "...", "coordinates": [...]}}, ...]}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> multi_polygon = '{"type": "MultiPolygon", "coordinates": [[[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]], [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]]]}'
        >>> result = asyncio.run(flatten(multi_polygon))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]]}}, ...]}'
    
    Notes:
        - 输入参数 geojson 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 多几何图形会被展平为对应的简单几何图形集合
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const result = turf.flatten(geojson);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@feature_conversion_mcp.tool
async def line_to_polygon(line: str, options: str = None) -> str:
    """
    将线转换为多边形。
    
    此功能将线几何图形转换为多边形几何图形，自动闭合线段的起点和终点。
    
    Args:
        line: GeoJSON 线特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON LineString 或 MultiLineString 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[125, -30], [145, -30], [145, -20], [125, -20], [125, -30]]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - properties: 传递给多边形的属性对象
                - autoComplete: 是否自动完成线段闭合
                - orderCoords: 是否重新排序坐标
                - mutate: 是否修改原始线特征
            - 示例: '{"properties": {"name": "converted polygon"}}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Polygon 或 MultiPolygon 特征
            - 类型: GeoJSON Feature with Polygon or MultiPolygon geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> line = '{"type": "LineString", "coordinates": [[125, -30], [145, -30], [145, -20], [125, -20], [125, -30]]}'
        >>> options = '{"properties": {"name": "converted polygon"}}'
        >>> result = asyncio.run(line_to_polygon(line, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[125, -30], [145, -30], [145, -20], [125, -20], [125, -30]]]}}'
    
    Notes:
        - 输入参数 line 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 线会自动闭合形成多边形边界
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const line = JSON.parse('{line}');
        const options = JSON.parse('{options_param}');
        const result = turf.lineToPolygon(line, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@feature_conversion_mcp.tool
async def polygonize(geojson: str) -> str:
    """
    将线几何图形转换为多边形。
    
    此功能将线或多线几何图形转换为多边形几何图形集合，基于线的闭合区域创建多边形。
    
    Args:
        geojson: GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON FeatureCollection, Geometry 或 Feature 规范，包含 LineString 或 MultiLineString
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]}}]}'
    
    Returns:
        str: JSON 字符串格式的多边形特征集合
            - 类型: GeoJSON FeatureCollection with Polygon features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}, ...]}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]}}]}'
        >>> result = asyncio.run(polygonize(geojson))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]}}]}'
    
    Notes:
        - 输入参数 geojson 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 基于线的闭合区域创建多边形
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const result = turf.polygonize(geojson);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@feature_conversion_mcp.tool
async def polygon_to_line(polygon: str) -> str:
    """
    将多边形转换为线几何图形。
    
    此功能将多边形或多边形几何图形转换为线或多线几何图形，提取多边形的边界。
    
    Args:
        polygon: GeoJSON 多边形特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Polygon 或 MultiPolygon 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Polygon", "coordinates": [[[125, -30], [145, -30], [145, -20], [125, -20], [125, -30]]]}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON LineString 或 MultiLineString 特征
            - 类型: GeoJSON Feature with LineString or MultiLineString geometry
            - 格式: {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> polygon = '{"type": "Polygon", "coordinates": [[[125, -30], [145, -30], [145, -20], [125, -20], [125, -30]]]}'
        >>> result = asyncio.run(polygon_to_line(polygon))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[125, -30], [145, -30], [145, -20], [125, -20], [125, -30]]}}'
    
    Notes:
        - 输入参数 polygon 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 提取多边形的边界作为线几何图形
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const polygon = JSON.parse('{polygon}');
        const result = turf.polygonToLine(polygon);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")
