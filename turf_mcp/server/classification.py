# 空间分类函数

from fastmcp import FastMCP

from turf_mcp.utils import call_js_script

classification_mcp = FastMCP("classification")

@classification_mcp.tool
async def nearestPoint(target_point: str, points: str) -> str:
    """
    查找距离目标点最近的点特征。
    
    此功能从点集合中查找距离给定目标点最近的点特征，并返回该点及其距离信息。
    
    Args:
        target_point: 目标点特征
            - 类型: str (JSON 字符串格式的 GeoJSON Feature)
            - 格式: Feature with Point geometry
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}'
        
        points: 点特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON FeatureCollection)
            - 格式: FeatureCollection with Point features
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.833, 39.284]}}, ...]}'
    
    Returns:
        str: JSON 字符串格式的最近点特征
            - 类型: GeoJSON Feature with Point geometry and distance property
            - 格式: {"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}, "properties": {"distance": 距离数值, ...}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.833, 39.284]}, "properties": {"distance": 12.34, ...}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> target_point = '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}'
        >>> points = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.833, 39.284]}}]}'
        >>> result = asyncio.run(nearestPoint(target_point, points))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.833, 39.284]}, "properties": {"distance": 12.34, ...}}'
    
    Notes:
        - 输入参数 target_point 和 points 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 计算的是球面距离，单位为千米
        - 返回的点特征包含原始属性以及新增的 distance 属性
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const targetPoint = JSON.parse('{target_point}');
        const points = JSON.parse('{points}');
        const result = turf.nearestPoint(targetPoint, points);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")
