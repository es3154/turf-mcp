# 空间连接和属性关联函数

from fastmcp import FastMCP

from turf_mcp.utils import call_js_script

joins_mcp = FastMCP("joins")

@joins_mcp.tool
async def pointsWithinPolygon(points: str, polygons: str) -> str:
    """
    查找多边形内部的点。
    
    此功能识别位于多边形或多边形集合内部的点特征，返回这些点特征。
    
    Args:
        points: 点特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON FeatureCollection)
            - 格式: FeatureCollection with Point features
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, ...]}'
        
        polygons: 多边形特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON FeatureCollection)
            - 格式: FeatureCollection with Polygon or MultiPolygon features
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[125, -15], [113, -22], [154, -27], [144, -15], [125, -15]]]}}, ...]}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Point features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}}, ...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> points = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}]}'
        >>> polygons = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[125, -15], [113, -22], [154, -27], [144, -15], [125, -15]]]}}]}'
        >>> result = asyncio.run(pointsWithinPolygon(points, polygons))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, ...]}'
    
    Notes:
        - 输入参数 points 和 polygons 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 仅返回位于多边形内部的点
        - 位于多边形边界上的点可能被视为内部或外部，取决于具体实现
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const points = JSON.parse('{points}');
        const polygons = JSON.parse('{polygons}');
        const result = turf.pointsWithinPolygon(points, polygons);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@joins_mcp.tool
async def tag(points: str, polygons: str, field: str, out_field: str) -> str:
    """
    为点特征添加多边形属性。
    
    此功能将多边形特征的属性值关联到位于多边形内部的点特征上。
    
    Args:
        points: 点特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON FeatureCollection)
            - 格式: FeatureCollection with Point features
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, ...]}'
        
        polygons: 多边形特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON FeatureCollection)
            - 格式: FeatureCollection with Polygon or MultiPolygon features
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[125, -15], [113, -22], [154, -27], [144, -15], [125, -15]]], "properties": {"name": "Area A"}}, ...]}'
        
        field: 源字段名
            - 类型: str
            - 描述: 多边形特征中要提取的属性字段名
            - 示例: 'name'
        
        out_field: 输出字段名
            - 类型: str
            - 描述: 点特征中要创建的属性字段名
            - 示例: 'area_name'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Point features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}, "properties": {...}}, ...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}, "properties": {"area_name": "Area A"}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> points = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}]}'
        >>> polygons = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[125, -15], [113, -22], [154, -27], [144, -15], [125, -15]]], "properties": {"name": "Area A"}}]}'
        >>> result = asyncio.run(tag(points, polygons, 'name', 'area_name'))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}, "properties": {"area_name": "Area A"}}, ...]}'
    
    Notes:
        - 输入参数 points 和 polygons 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 仅对位于多边形内部的点添加属性
        - 如果一个点位于多个多边形内，将使用最后一个匹配的多边形属性
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const points = JSON.parse('{points}');
        const polygons = JSON.parse('{polygons}');
        const field = '{field}';
        const outField = '{out_field}';
        const result = turf.tag(points, polygons, field, outField);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")
