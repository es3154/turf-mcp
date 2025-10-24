# 空间聚合和聚类函数

from fastmcp import FastMCP

from turf_mcp.utils import call_js_script

aggregation_mcp = FastMCP("aggregation")

@aggregation_mcp.tool
async def collect(polygons: str, points: str, in_field: str, out_field: str) -> str:
    """
    将点属性聚合到多边形中。
    
    此功能将位于多边形内部的点的属性值聚合到多边形中，用于统计和汇总分析。
    
    Args:
        polygons: 多边形特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON FeatureCollection)
            - 格式: FeatureCollection with Polygon or MultiPolygon features
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[125, -15], [113, -22], [154, -27], [144, -15], [125, -15]]]}}, ...]}'
        
        points: 点特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON FeatureCollection)
            - 格式: FeatureCollection with Point features
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984], "properties": {"population": 100}}, ...]}'
        
        in_field: 输入字段名
            - 类型: str
            - 描述: 点特征中要聚合的属性字段名
            - 示例: 'population'
        
        out_field: 输出字段名
            - 类型: str
            - 描述: 多边形特征中要创建的聚合属性字段名
            - 示例: 'total_population'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Polygon features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}, "properties": {..., "total_population": 聚合值}}, ...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}, "properties": {"total_population": 1500}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> polygons = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[125, -15], [113, -22], [154, -27], [144, -15], [125, -15]]]}}]}'
        >>> points = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984], "properties": {"population": 100}}]}'
        >>> result = asyncio.run(collect(polygons, points, 'population', 'total_population'))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}, "properties": {"total_population": 100}}, ...]}'
    
    Notes:
        - 输入参数 polygons 和 points 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 仅对位于多边形内部的点进行属性聚合
        - 聚合方式为求和，即计算多边形内部所有点的属性值总和
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const polygons = JSON.parse('{polygons}');
        const points = JSON.parse('{points}');
        const inField = '{in_field}';
        const outField = '{out_field}';
        const result = turf.collect(polygons, points, inField, outField);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@aggregation_mcp.tool
async def clustersDbscan(points: str, max_distance: float, options: str = None) -> str:
    """
    使用 DBSCAN 算法进行点聚类。
    
    此功能使用基于密度的空间聚类算法 (DBSCAN) 对点进行聚类，识别密集区域。
    
    Args:
        points: 点特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON FeatureCollection)
            - 格式: FeatureCollection with Point features
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, ...]}'
        
        max_distance: 最大距离
            - 类型: float
            - 描述: 聚类搜索的最大距离（单位：千米）
            - 示例: 100.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
                - minPoints: 形成聚类所需的最小点数 (默认: 3)
            - 示例: '{"units": "miles", "minPoints": 5}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Point features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}, "properties": {"cluster": 聚类编号, ...}}, ...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}, "properties": {"cluster": 1}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> points = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}]}'
        >>> result = asyncio.run(clustersDbscan(points, 100.0, '{"minPoints": 3}'))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}, "properties": {"cluster": 1}}, ...]}'
    
    Notes:
        - 输入参数 points 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - DBSCAN 算法能够识别任意形状的聚类，并处理噪声点
        - 聚类编号从 0 开始，-1 表示噪声点（不属于任何聚类）
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const points = JSON.parse('{points}');
        const maxDistance = parseFloat({max_distance});
        const options = JSON.parse('{options_param}');
        const result = turf.clustersDbscan(points, maxDistance, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@aggregation_mcp.tool
async def clustersKmeans(points: str, number_of_clusters: int, options: str = None) -> str:
    """
    使用 K-means 算法进行点聚类。
    
    此功能使用 K-means 聚类算法对点进行聚类，将点划分为指定数量的簇。
    
    Args:
        points: 点特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON FeatureCollection)
            - 格式: FeatureCollection with Point features
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, ...]}'
        
        number_of_clusters: 聚类数量
            - 类型: int
            - 描述: 要创建的聚类数量
            - 示例: 5
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - numberOfClusters: 聚类数量（与 number_of_clusters 参数相同）
                - mutate: 是否修改原始特征 (默认: false)
            - 示例: '{"mutate": true}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Point features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}, "properties": {"cluster": 聚类编号, ...}}, ...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}, "properties": {"cluster": 1}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> points = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}]}'
        >>> result = asyncio.run(clustersKmeans(points, 5))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}, "properties": {"cluster": 1}}, ...]}'
    
    Notes:
        - 输入参数 points 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - K-means 算法需要预先指定聚类数量
        - 聚类编号从 0 开始
        - 算法使用随机初始中心点，每次运行结果可能不同
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const points = JSON.parse('{points}');
        const numberOfClusters = parseInt({number_of_clusters});
        const options = JSON.parse('{options_param}');
        const result = turf.clustersKmeans(points, numberOfClusters, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")
