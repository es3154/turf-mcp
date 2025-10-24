# 几何对象创建辅助函数

from fastmcp import FastMCP

from turf_mcp.utils import call_js_script

helper_mcp = FastMCP("helper")

@helper_mcp.tool
async def featureCollection(features: str, options: str = None) -> str:
    """
    将多个地理特征组合成一个特征集合。
    
    此功能将一组地理特征组合成一个统一的特征集合，便于批量处理和管理多个地理对象。
    
    Args:
        features: 特征数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: 包含 GeoJSON 特征的数组
            - 示例: '[{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.833, 39.284]}}]'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - bbox: 边界框数组 [minX, minY, maxX, maxY]
                - id: 特征集合的标识符
            - 示例: '{"bbox": [-76, 39, -75, 40], "id": "collection1"}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection
            - 格式: {"type": "FeatureCollection", "features": [...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> features = '[{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.833, 39.284]}}]'
        >>> result = asyncio.run(featureCollection(features))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, ...]}'
    
    Notes:
        - 输入参数 features 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 特征集合是组织和管理多个地理对象的有效方式
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const features = JSON.parse('{features}');
        const options = JSON.parse('{options_param}');
        const result = turf.featureCollection(features, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@helper_mcp.tool
async def feature(geometry: str, properties: str = None, options: str = None) -> str:
    """
    创建单个地理特征对象。
    
    此功能将几何图形和属性信息组合成一个完整的地理特征，用于表示具体的地理要素。
    
    Args:
        geometry: 几何图形对象
            - 类型: str (JSON 字符串格式的 GeoJSON 几何图形)
            - 格式: 任何有效的 GeoJSON 几何图形
            - 示例: '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        
        properties: 属性对象
            - 类型: str (JSON 字符串) 或 None
            - 格式: 键值对对象
            - 示例: '{"name": "Location A", "type": "landmark"}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - bbox: 边界框数组 [minX, minY, maxX, maxY]
                - id: 特征的标识符
            - 示例: '{"bbox": [-75.5, 39.5, -75, 40], "id": "feature1"}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Feature
            - 类型: GeoJSON Feature
            - 格式: {"type": "Feature", "geometry": {...}, "properties": {...}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}, "properties": {"name": "Location A"}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geometry = '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        >>> properties = '{"name": "Location A"}'
        >>> result = asyncio.run(feature(geometry, properties))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}, "properties": {"name": "Location A"}}'
    
    Notes:
        - 输入参数 geometry、properties 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 特征是 GeoJSON 中的基本数据单元，包含几何信息和属性
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    properties_param = properties if properties else '{}'
    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const geometry = JSON.parse('{geometry}');
        const properties = JSON.parse('{properties_param}');
        const options = JSON.parse('{options_param}');
        const result = turf.feature(geometry, properties, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@helper_mcp.tool
async def geometryCollection(geometries: str, properties: str = None, options: str = None) -> str:
    """
    创建几何图形集合特征。
    
    此功能将多个不同类型的几何图形组合成一个几何集合特征，适用于包含多种几何类型的复杂场景。
    
    Args:
        geometries: 几何图形数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: 包含 GeoJSON 几何图形的数组
            - 示例: '[{"type": "Point", "coordinates": [100, 0]}, {"type": "LineString", "coordinates": [[101, 0], [102, 1]]}]'
        
        properties: 属性对象
            - 类型: str (JSON 字符串) 或 None
            - 格式: 键值对对象
            - 示例: '{"name": "mixed geometries"}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - bbox: 边界框数组 [minX, minY, maxX, maxY]
                - id: 特征的标识符
            - 示例: '{"bbox": [99, -1, 103, 2], "id": "geometry_collection"}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Feature with GeometryCollection
            - 类型: GeoJSON Feature with GeometryCollection geometry
            - 格式: {"type": "Feature", "geometry": {"type": "GeometryCollection", "geometries": [...]}, "properties": {...}}
            - 示例: '{"type": "Feature", "geometry": {"type": "GeometryCollection", "geometries": [{"type": "Point", "coordinates": [100, 0]}, ...]}, "properties": {"name": "mixed geometries"}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geometries = '[{"type": "Point", "coordinates": [100, 0]}, {"type": "LineString", "coordinates": [[101, 0], [102, 1]]}]'
        >>> properties = '{"name": "mixed geometries"}'
        >>> result = asyncio.run(geometryCollection(geometries, properties))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "GeometryCollection", "geometries": [...]}, "properties": {"name": "mixed geometries"}}'
    
    Notes:
        - 输入参数 geometries、properties 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 几何集合可以包含不同类型的几何图形
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    properties_param = properties if properties else '{}'
    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const geometries = JSON.parse('{geometries}');
        const properties = JSON.parse('{properties_param}');
        const options = JSON.parse('{options_param}');
        const result = turf.geometryCollection(geometries, properties, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@helper_mcp.tool
async def lineString(coordinates: str, properties: str = None, options: str = None) -> str:
    """
    创建线特征对象。
    
    此功能根据坐标点数组创建线特征，用于表示路径、边界等线性地理要素。
    
    Args:
        coordinates: 坐标点数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: [[lng1, lat1], [lng2, lat2], ...]
            - 示例: '[[-74, 40], [-78, 42], [-82, 35]]'
        
        properties: 属性对象
            - 类型: str (JSON 字符串) 或 None
            - 格式: 键值对对象
            - 示例: '{"name": "route", "type": "highway"}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - bbox: 边界框数组 [minX, minY, maxX, maxY]
                - id: 特征的标识符
            - 示例: '{"bbox": [-83, 34, -73, 43], "id": "line1"}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON LineString Feature
            - 类型: GeoJSON Feature with LineString geometry
            - 格式: {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}, "properties": {...}}
            - 示例: '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-74, 40], [-78, 42], [-82, 35]]}, "properties": {"name": "route"}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> coordinates = '[[-74, 40], [-78, 42], [-82, 35]]'
        >>> properties = '{"name": "route"}'
        >>> result = asyncio.run(lineString(coordinates, properties))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-74, 40], [-78, 42], [-82, 35]]}, "properties": {"name": "route"}}'
    
    Notes:
        - 输入参数 coordinates、properties 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 至少需要两个坐标点才能创建有效的线
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    properties_param = properties if properties else '{}'
    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const coordinates = JSON.parse('{coordinates}');
        const properties = JSON.parse('{properties_param}');
        const options = JSON.parse('{options_param}');
        const result = turf.lineString(coordinates, properties, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@helper_mcp.tool
async def multiLineString(coordinates: str, properties: str = None, options: str = None) -> str:
    """
    创建多线特征对象。
    
    此功能根据多组坐标点数组创建多线特征，用于表示包含多条线的复杂线性要素。
    
    Args:
        coordinates: 多线坐标数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: [[[lng1, lat1], [lng2, lat2], ...], [[lng3, lat3], [lng4, lat4], ...]]
            - 示例: '[[[[-24, 63], [-23, 60], [-25, 65], [-20, 69]]], [[[-14, 43], [-13, 40], [-15, 45], [-10, 49]]]]'
        
        properties: 属性对象
            - 类型: str (JSON 字符串) 或 None
            - 格式: 键值对对象
            - 示例: '{"name": "multi route"}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - bbox: 边界框数组 [minX, minY, maxX, maxY]
                - id: 特征的标识符
            - 示例: '{"bbox": [-26, 39, -9, 70], "id": "multi_line1"}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON MultiLineString Feature
            - 类型: GeoJSON Feature with MultiLineString geometry
            - 格式: {"type": "Feature", "geometry": {"type": "MultiLineString", "coordinates": [...]}, "properties": {...}}
            - 示例: '{"type": "Feature", "geometry": {"type": "MultiLineString", "coordinates": [[[-24, 63], [-23, 60], ...], [[-14, 43], [-13, 40], ...]]}, "properties": {"name": "multi route"}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> coordinates = '[[[[-24, 63], [-23, 60], [-25, 65], [-20, 69]]], [[[-14, 43], [-13, 40], [-15, 45], [-10, 49]]]]'
        >>> properties = '{"name": "multi route"}'
        >>> result = asyncio.run(multiLineString(coordinates, properties))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "MultiLineString", "coordinates": [...]}, "properties": {"name": "multi route"}}'
    
    Notes:
        - 输入参数 coordinates、properties 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 多线特征包含多条独立的线
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    properties_param = properties if properties else '{}'
    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const coordinates = JSON.parse('{coordinates}');
        const properties = JSON.parse('{properties_param}');
        const options = JSON.parse('{options_param}');
        const result = turf.multiLineString(coordinates, properties, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@helper_mcp.tool
async def multiPoint(coordinates: str, properties: str = None, options: str = None) -> str:
    """
    创建多点特征对象。
    
    此功能根据坐标点数组创建多点特征，用于表示一组相关的点要素。
    
    Args:
        coordinates: 多点坐标数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: [[lng1, lat1], [lng2, lat2], ...]
            - 示例: '[[0, 0], [10, 10]]'
        
        properties: 属性对象
            - 类型: str (JSON 字符串) 或 None
            - 格式: 键值对对象
            - 示例: '{"name": "point group"}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - bbox: 边界框数组 [minX, minY, maxX, maxY]
                - id: 特征的标识符
            - 示例: '{"bbox": [-1, -1, 11, 11], "id": "multi_point1"}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON MultiPoint Feature
            - 类型: GeoJSON Feature with MultiPoint geometry
            - 格式: {"type": "Feature", "geometry": {"type": "MultiPoint", "coordinates": [...]}, "properties": {...}}
            - 示例: '{"type": "Feature", "geometry": {"type": "MultiPoint", "coordinates": [[0, 0], [10, 10]]}, "properties": {"name": "point group"}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> coordinates = '[[0, 0], [10, 10]]'
        >>> properties = '{"name": "point group"}'
        >>> result = asyncio.run(multiPoint(coordinates, properties))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "MultiPoint", "coordinates": [[0, 0], [10, 10]]}, "properties": {"name": "point group"}}'
    
    Notes:
        - 输入参数 coordinates、properties 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 多点特征包含多个独立的点
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    properties_param = properties if properties else '{}'
    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const coordinates = JSON.parse('{coordinates}');
        const properties = JSON.parse('{properties_param}');
        const options = JSON.parse('{options_param}');
        const result = turf.multiPoint(coordinates, properties, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@helper_mcp.tool
async def multiPolygon(coordinates: str, properties: str = None, options: str = None) -> str:
    """
    创建多多边形特征对象。
    
    此功能根据多组多边形坐标数组创建多多边形特征，用于表示包含多个多边形的复杂区域要素。
    
    Args:
        coordinates: 多多边形坐标数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: [[[[lng1, lat1], [lng2, lat2], ...]], [[[lng3, lat3], [lng4, lat4], ...]]]
            - 示例: '[[[[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]]], [[[[10, 0], [10, 5], [15, 5], [15, 0], [10, 0]]]]]'
        
        properties: 属性对象
            - 类型: str (JSON 字符串) 或 None
            - 格式: 键值对对象
            - 示例: '{"name": "multi area"}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - bbox: 边界框数组 [minX, minY, maxX, maxY]
                - id: 特征的标识符
            - 示例: '{"bbox": [-1, -1, 16, 11], "id": "multi_polygon1"}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON MultiPolygon Feature
            - 类型: GeoJSON Feature with MultiPolygon geometry
            - 格式: {"type": "Feature", "geometry": {"type": "MultiPolygon", "coordinates": [...]}, "properties": {...}}
            - 示例: '{"type": "Feature", "geometry": {"type": "MultiPolygon", "coordinates": [[[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]], [[[10, 0], [10, 5], [15, 5], [15, 0], [10, 0]]]]}, "properties": {"name": "multi area"}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> coordinates = '[[[[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]]], [[[[10, 0], [10, 5], [15, 5], [15, 0], [10, 0]]]]]'
        >>> properties = '{"name": "multi area"}'
        >>> result = asyncio.run(multiPolygon(coordinates, properties))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "MultiPolygon", "coordinates": [...]}, "properties": {"name": "multi area"}}'
    
    Notes:
        - 输入参数 coordinates、properties 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 多多边形特征包含多个独立的多边形
        - 每个多边形必须形成闭合环
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    properties_param = properties if properties else '{}'
    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const coordinates = JSON.parse('{coordinates}');
        const properties = JSON.parse('{properties_param}');
        const options = JSON.parse('{options_param}');
        const result = turf.multiPolygon(coordinates, properties, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@helper_mcp.tool
async def point(coordinates: str, properties: str = None, options: str = None) -> str:
    """
    创建点特征对象。
    
    此功能根据坐标点创建点特征，用于表示具体的地理位置点。
    
    Args:
        coordinates: 坐标点
            - 类型: str (JSON 字符串格式的数组)
            - 格式: [lng, lat]
            - 示例: '[-75.343, 39.984]'
        
        properties: 属性对象
            - 类型: str (JSON 字符串) 或 None
            - 格式: 键值对对象
            - 示例: '{"name": "Location A", "type": "city"}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - bbox: 边界框数组 [minX, minY, maxX, maxY]
                - id: 特征的标识符
            - 示例: '{"bbox": [-75.5, 39.5, -75, 40], "id": "point1"}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Point Feature
            - 类型: GeoJSON Feature with Point geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}, "properties": {...}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}, "properties": {"name": "Location A"}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> coordinates = '[-75.343, 39.984]'
        >>> properties = '{"name": "Location A"}'
        >>> result = asyncio.run(point(coordinates, properties))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}, "properties": {"name": "Location A"}}'
    
    Notes:
        - 输入参数 coordinates、properties 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 点特征是地理信息系统中最基本的要素类型
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    properties_param = properties if properties else '{}'
    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const coordinates = JSON.parse('{coordinates}');
        const properties = JSON.parse('{properties_param}');
        const options = JSON.parse('{options_param}');
        const result = turf.point(coordinates, properties, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@helper_mcp.tool
async def polygon(coordinates: str, properties: str = None, options: str = None) -> str:
    """
    创建多边形特征对象。
    
    此功能根据坐标点数组创建多边形特征，用于表示区域、地块等面状地理要素。
    
    Args:
        coordinates: 多边形坐标数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: [[[lng1, lat1], [lng2, lat2], [lng3, lat3], [lng1, lat1]]]
            - 示例: '[[[125, -15], [113, -22], [154, -27], [144, -15], [125, -15]]]'
        
        properties: 属性对象
            - 类型: str (JSON 字符串) 或 None
            - 格式: 键值对对象
            - 示例: '{"name": "area", "type": "park"}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - bbox: 边界框数组 [minX, minY, maxX, maxY]
                - id: 特征的标识符
            - 示例: '{"bbox": [112, -28, 155, -14], "id": "polygon1"}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Polygon Feature
            - 类型: GeoJSON Feature with Polygon geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}, "properties": {...}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[125, -15], [113, -22], [154, -27], [144, -15], [125, -15]]]}, "properties": {"name": "area"}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> coordinates = '[[[125, -15], [113, -22], [154, -27], [144, -15], [125, -15]]]'
        >>> properties = '{"name": "area"}'
        >>> result = asyncio.run(polygon(coordinates, properties))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[125, -15], [113, -22], [154, -27], [144, -15], [125, -15]]]}, "properties": {"name": "area"}}'
    
    Notes:
        - 输入参数 coordinates、properties 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 多边形必须形成闭合环，首尾坐标点必须相同
        - 支持带孔的多边形（多个环）
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    properties_param = properties if properties else '{}'
    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const coordinates = JSON.parse('{coordinates}');
        const properties = JSON.parse('{properties_param}');
        const options = JSON.parse('{options_param}');
        const result = turf.polygon(coordinates, properties, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")
