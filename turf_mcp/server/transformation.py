# 几何变换和操作函数

from fastmcp import FastMCP

from turf_mcp.utils import call_js_script

transformation_mcp = FastMCP("transformation")

@transformation_mcp.tool
async def bboxClip(feature: str, bbox: str) -> str:
    """
    将 GeoJSON 特征裁剪到指定的边界框内。
    
    此功能将输入的 GeoJSON 特征（线或多边形）裁剪到给定的边界框范围内，只保留边界框内的部分。
    
    Args:
        feature: GeoJSON 特征
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Feature 规范，支持 LineString、MultiLineString、Polygon、MultiPolygon
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[2, 2], [8, 4], [12, 8], [3, 7], [2, 2]]]}}'
        
        bbox: 边界框数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: [minX, minY, maxX, maxY]
            - 示例: '[0, 0, 10, 10]'
    
    Returns:
        str: JSON 字符串格式的裁剪后的 GeoJSON 特征
            - 类型: GeoJSON Feature with LineString, MultiLineString, Polygon, or MultiPolygon geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[2, 2], [8, 4], [10, 8], [3, 7], [2, 2]]]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> feature = '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[2, 2], [8, 4], [12, 8], [3, 7], [2, 2]]]}}'
        >>> bbox = '[0, 0, 10, 10]'
        >>> result = asyncio.run(bboxClip(feature, bbox))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[2, 2], [8, 4], [10, 8], [3, 7], [2, 2]]]}}'
    
    Notes:
        - 输入参数 feature 和 bbox 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 裁剪多边形时可能会产生退化边
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const feature = JSON.parse('{feature}');
        const bbox = JSON.parse('{bbox}');
        const result = turf.bboxClip(feature, bbox);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def bezierSpline(line: str, options: str = None) -> str:
    """
    将直线转换为平滑的贝塞尔曲线。
    
    此功能将输入的直线路径转换为平滑的曲线路径，使线条更加流畅自然。
    
    Args:
        line: GeoJSON LineString 特征
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON LineString 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-76.091308, 18.427501], [-76.695556, 18.729501], [-76.552734, 19.40443]]}}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - resolution: 分辨率控制点数 (默认: 10000)
                - sharpness: 控制曲线锐度的参数 (默认: 0.85)
            - 示例: '{"resolution": 20000, "sharpness": 0.5}'
    
    Returns:
        str: JSON 字符串格式的贝塞尔样条曲线 GeoJSON LineString 特征
            - 类型: GeoJSON Feature with LineString geometry
            - 格式: {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-76.091308, 18.427501], [-76.5, 19.0], [-76.695556, 18.729501]]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> line = '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-76.091308, 18.427501], [-76.695556, 18.729501], [-76.552734, 19.40443]]}}'
        >>> options = '{"resolution": 20000, "sharpness": 0.5}'
        >>> result = asyncio.run(bezierSpline(line, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-76.091308, 18.427501], [-76.5, 19.0], [-76.695556, 18.729501]]}}'
    
    Notes:
        - 输入参数 line 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 生成的曲线会平滑原始 LineString 的路径
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const line = JSON.parse('{line}');
        const options = JSON.parse('{options_param}');
        const result = turf.bezierSpline(line, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def circle(center: str, radius: float, options: str = None) -> str:
    """
    根据中心点和半径创建圆形区域。
    
    此功能以指定的中心点和半径生成一个圆形多边形区域，可以控制圆形的平滑度和单位。
    
    Args:
        center: 中心点 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范或坐标数组
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-75.343, 39.984]}' 或 '[-75.343, 39.984]'
        
        radius: 圆的半径
            - 类型: float
            - 描述: 圆的半径值
            - 示例: 5.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - steps: 圆的边数 (默认: 64)
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
                - properties: 传递给圆形多边形的属性对象
            - 示例: '{"steps": 32, "units": "miles", "properties": {"name": "circle"}}'
    
    Returns:
        str: JSON 字符串格式的圆形 GeoJSON Polygon 特征
            - 类型: GeoJSON Feature with Polygon geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-75.35, 39.99], [-75.34, 39.99], ...]]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> center = '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        >>> options = '{"steps": 32, "units": "miles"}'
        >>> result = asyncio.run(circle(center, 5.0, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-75.35, 39.99], [-75.34, 39.99], ...]]}}'
    
    Notes:
        - 输入参数 center 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - steps 参数控制圆的平滑度，值越大圆越平滑
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const center = JSON.parse('{center}');
        const radius = parseFloat({radius});
        const options = JSON.parse('{options_param}');
        const result = turf.circle(center, radius, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def clone(geojson: str) -> str:
    """
    创建 GeoJSON 对象的完整副本。
    
    此功能创建输入 GeoJSON 对象的深拷贝，包括所有属性和几何信息。
    
    Args:
        geojson: GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-74, 40], [-78, 42], [-82, 35]]}, "properties": {"color": "red"}}'
    
    Returns:
        str: JSON 字符串格式的克隆后的 GeoJSON 对象
            - 类型: 与输入相同的 GeoJSON 类型
            - 格式: 与输入相同的格式，包含所有属性和外成员
            - 示例: '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-74, 40], [-78, 42], [-82, 35]]}, "properties": {"color": "red"}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson = '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-74, 40], [-78, 42], [-82, 35]]}, "properties": {"color": "red"}}'
        >>> result = asyncio.run(clone(geojson))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-74, 40], [-78, 42], [-82, 35]]}, "properties": {"color": "red"}}'
    
    Notes:
        - 输入参数 geojson 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 此方法比 JSON.parse + JSON.stringify 更快
        - 包含所有可能的"外成员"（非标准属性）
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const result = turf.clone(geojson);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def concave(points: str, options: str = None) -> str:
    """
    计算点集的凹包。
    
    该函数使用 Turf.js 库的 concave 方法，从一组点生成凹包多边形。
    
    Args:
        points: 点集 GeoJSON FeatureCollection
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON FeatureCollection 规范，包含 Point 特征
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-63.601226, 44.642643]}}, ...]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - maxEdge: 凹包边缘的最大长度 (默认: Infinity)
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
            - 示例: '{"maxEdge": 1, "units": "miles"}'
    
    Returns:
        str: JSON 字符串格式的凹包 GeoJSON Polygon 或 MultiPolygon 特征
            - 类型: GeoJSON Feature with Polygon or MultiPolygon geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}} 或 null（如果无法计算）
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-63.6, 44.64], [-63.59, 44.65], ...]]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> points = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-63.601226, 44.642643]}}]}'
        >>> options = '{"maxEdge": 1, "units": "miles"}'
        >>> result = asyncio.run(concave(points, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-63.6, 44.64], [-63.59, 44.65], ...]]}}'
    
    Notes:
        - 输入参数 points 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 内部使用 turf-tin 生成几何图形
        - 如果无法计算凹包，返回 null
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const points = JSON.parse('{points}');
        const options = JSON.parse('{options_param}');
        const result = turf.concave(points, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def convex(points: str) -> str:
    """
    计算点集的凸包。
    
    该函数使用 Turf.js 库的 convex 方法，从一组点生成凸包多边形。
    
    Args:
        points: 点集 GeoJSON FeatureCollection
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON FeatureCollection 规范，包含 Point 特征
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [10.195312, 43.755225]}}, ...]}'
    
    Returns:
        str: JSON 字符串格式的凸包 GeoJSON Polygon 特征
            - 类型: GeoJSON Feature with Polygon geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[10.195312, 43.755225], [10.404052, 43.8424511], ...]]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> points = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [10.195312, 43.755225]}}]}'
        >>> result = asyncio.run(convex(points))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[10.195312, 43.755225], [10.404052, 43.8424511], ...]]}}'
    
    Notes:
        - 输入参数 points 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 凸包是包含所有点的最小凸多边形
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const points = JSON.parse('{points}');
        const result = turf.convex(points);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def difference(featureCollection: str) -> str:
    """
    计算两个多边形的差异。
    
    该函数使用 Turf.js 库的 difference 方法，计算两个多边形的几何差异。
    
    Args:
        featureCollection: 包含两个多边形的 GeoJSON FeatureCollection
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON FeatureCollection 规范，包含两个 Polygon 特征
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[128, -26], [141, -26], [141, -21], [128, -21], [128, -26]]]}}, {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[126, -28], [140, -28], [140, -20], [126, -20], [126, -28]]]}}]}'
    
    Returns:
        str: JSON 字符串格式的差异 GeoJSON Feature
            - 类型: GeoJSON Feature with Polygon or MultiPolygon geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[128, -26], [141, -26], ...]]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> featureCollection = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[128, -26], [141, -26], [141, -21], [128, -21], [128, -26]]]}}, {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[126, -28], [140, -28], [140, -20], [126, -20], [126, -28]]]}}]}'
        >>> result = asyncio.run(difference(featureCollection))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[128, -26], [141, -26], ...]]}}'
    
    Notes:
        - 输入参数 featureCollection 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 计算第一个多边形与第二个多边形的差异
        - 返回第一个多边形中不在第二个多边形中的部分
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const featureCollection = JSON.parse('{featureCollection}');
        const result = turf.difference(featureCollection);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def dissolve(featureCollection: str, options: str = None) -> str:
    """
    合并相邻的多边形。
    
    该函数使用 Turf.js 库的 dissolve 方法，合并相邻的多边形特征。
    
    Args:
        featureCollection: 多边形特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON FeatureCollection 规范，包含 Polygon 特征
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]}}, {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0, -1], [0, 0], [1, 0], [1, -1], [0,-1]]]}}]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - propertyName: 用于分组合并的属性名称
            - 示例: '{"propertyName": "combine"}'
    
    Returns:
        str: JSON 字符串格式的合并后的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Polygon features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0, -1], [0, 1], [1, 1], [1, -1], [0, -1]]]}}]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> featureCollection = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]}}, {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0, -1], [0, 0], [1, 0], [1, -1], [0,-1]]]}}]}'
        >>> options = '{"propertyName": "combine"}'
        >>> result = asyncio.run(dissolve(featureCollection, options))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0, -1], [0, 1], [1, 1], [1, -1], [0, -1]]]}}]}'
    
    Notes:
        - 输入参数 featureCollection 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 不支持 MultiPolygon 特征
        - 如果提供 propertyName，只有具有相同属性值的多边形才会被合并
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const featureCollection = JSON.parse('{featureCollection}');
        const options = JSON.parse('{options_param}');
        const result = turf.dissolve(featureCollection, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def intersect(featureCollection: str) -> str:
    """
    计算多边形的交集。
    
    该函数使用 Turf.js 库的 intersect 方法，计算两个多边形的几何交集。
    
    Args:
        featureCollection: 包含两个多边形的 GeoJSON FeatureCollection
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON FeatureCollection 规范，包含两个 Polygon 特征
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-122.801742, 45.48565], [-122.801742, 45.60491], [-122.584762, 45.60491], [-122.584762, 45.48565], [-122.801742, 45.48565]]]}}, {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-122.520217, 45.535693], [-122.64038, 45.553967], [-122.720031, 45.526554], [-122.669906, 45.507309], [-122.723464, 45.446643], [-122.532577, 45.408574], [-122.487258, 45.477466], [-122.520217, 45.535693]]]}}]}'
    
    Returns:
        str: JSON 字符串格式的交集 GeoJSON Feature
            - 类型: GeoJSON Feature with Polygon or MultiPolygon geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}} 或 null（如果没有交集）
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-122.6, 45.5], [-122.5, 45.5], ...]]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> featureCollection = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-122.801742, 45.48565], [-122.801742, 45.60491], [-122.584762, 45.60491], [-122.584762, 45.48565], [-122.801742, 45.48565]]]}}, {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-122.520217, 45.535693], [-122.64038, 45.553967], [-122.720031, 45.526554], [-122.669906, 45.507309], [-122.723464, 45.446643], [-122.532577, 45.408574], [-122.487258, 45.477466], [-122.520217, 45.535693]]]}}]}'
        >>> result = asyncio.run(intersect(featureCollection))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-122.6, 45.5], [-122.5, 45.5], ...]]}}'
    
    Notes:
        - 输入参数 featureCollection 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 如果没有交集，返回 null
        - 交集可以是 Point、LineString、Polygon 或 Multi* 几何类型
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const featureCollection = JSON.parse('{featureCollection}');
        const result = turf.intersect(featureCollection);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def lineOffset(line: str, distance: float, options: str = None) -> str:
    """
    计算线的偏移。
    
    该函数使用 Turf.js 库的 lineOffset 方法，计算给定线的偏移线。
    
    Args:
        line: GeoJSON LineString 或 MultiLineString 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON LineString 或 MultiLineString 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[-74, 40], [-78, 42], [-82, 35]]}'
        
        distance: 偏移距离
            - 类型: float
            - 描述: 线的偏移距离，可以为负值
            - 示例: 10.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
            - 示例: '{"units": "miles"}'
    
    Returns:
        str: JSON 字符串格式的偏移线 GeoJSON Feature
            - 类型: GeoJSON Feature with LineString or MultiLineString geometry
            - 格式: {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-74.1, 40.1], [-78.1, 42.1], [-82.1, 35.1]]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> line = '{"type": "LineString", "coordinates": [[-74, 40], [-78, 42], [-82, 35]]}'
        >>> options = '{"units": "miles"}'
        >>> result = asyncio.run(lineOffset(line, 10.0, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-74.1, 40.1], [-78.1, 42.1], [-82.1, 35.1]]}}'
    
    Notes:
        - 输入参数 line 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 距离可以为负值，表示相反方向的偏移
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const line = JSON.parse('{line}');
        const distance = parseFloat({distance});
        const options = JSON.parse('{options_param}');
        const result = turf.lineOffset(line, distance, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def simplify(geojson: str, options: str = None) -> str:
    """
    简化 GeoJSON 几何。
    
    该函数使用 Turf.js 库的 simplify 方法，简化给定的 GeoJSON 几何图形。
    
    Args:
        geojson: GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Polygon", "coordinates": [[[-70.603637, -33.399918], [-70.614624, -33.395332], [-70.639343, -33.392466], [-70.659942, -33.394759], [-70.683975, -33.404504], [-70.697021, -33.419406], [-70.701141, -33.434306], [-70.700454, -33.446339], [-70.694274, -33.458369], [-70.682601, -33.465816], [-70.668869, -33.472117], [-70.646209, -33.473835], [-70.624923, -33.472117], [-70.609817, -33.468107], [-70.595397, -33.458369], [-70.587158, -33.442901], [-70.587158, -33.426283], [-70.590591, -33.414248], [-70.594711, -33.406224], [-70.603637, -33.399918]]]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - tolerance: 简化容差 (默认: 1)
                - highQuality: 是否使用高质量简化 (默认: false)
                - mutate: 是否允许修改输入对象 (默认: false)
            - 示例: '{"tolerance": 0.01, "highQuality": true}'
    
    Returns:
        str: JSON 字符串格式的简化后的 GeoJSON 对象
            - 类型: 与输入相同的 GeoJSON 类型
            - 格式: 与输入相同的格式
            - 示例: '{"type": "Polygon", "coordinates": [[[-70.603637, -33.399918], [-70.614624, -33.395332], [-70.639343, -33.392466], ...]]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson = '{"type": "Polygon", "coordinates": [[[-70.603637, -33.399918], [-70.614624, -33.395332], [-70.639343, -33.392466], [-70.659942, -33.394759], [-70.683975, -33.404504], [-70.697021, -33.419406], [-70.701141, -33.434306], [-70.700454, -33.446339], [-70.694274, -33.458369], [-70.682601, -33.465816], [-70.668869, -33.472117], [-70.646209, -33.473835], [-70.624923, -33.472117], [-70.609817, -33.468107], [-70.595397, -33.458369], [-70.587158, -33.442901], [-70.587158, -33.426283], [-70.590591, -33.414248], [-70.594711, -33.406224], [-70.603637, -33.399918]]]}'
        >>> options = '{"tolerance": 0.01, "highQuality": true}'
        >>> result = asyncio.run(simplify(geojson, options))
        >>> print(result)
        '{"type": "Polygon", "coordinates": [[[-70.603637, -33.399918], [-70.614624, -33.395332], [-70.639343, -33.392466], ...]]}'
    
    Notes:
        - 输入参数 geojson 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - tolerance 值越小，简化程度越低
        - highQuality 为 true 时使用更精确但更慢的算法
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const options = JSON.parse('{options_param}');
        const result = turf.simplify(geojson, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def tesselate(polygon: str) -> str:
    """
    将多边形分割为三角形。
    
    该函数使用 Turf.js 库的 tesselate 方法，将给定的多边形分割为三角形集合。
    
    Args:
        polygon: GeoJSON Polygon 特征
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Polygon 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[11, 0], [22, 4], [31, 0], [31, 11], [21, 15], [11, 11], [11, 0]]]}}'
    
    Returns:
        str: JSON 字符串格式的三角形集合 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Polygon features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[11, 0], [22, 4], [31, 0], [11, 0]]]}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> polygon = '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[11, 0], [22, 4], [31, 0], [31, 11], [21, 15], [11, 11], [11, 0]]]}}'
        >>> result = asyncio.run(tesselate(polygon))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[11, 0], [22, 4], [31, 0], [11, 0]]]}}, ...]}'
    
    Notes:
        - 输入参数 polygon 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 返回的三角形集合覆盖原始多边形的整个区域
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const polygon = JSON.parse('{polygon}');
        const result = turf.tesselate(polygon);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def transformRotate(geojson: str, angle: float, options: str = None) -> str:
    """
    旋转 GeoJSON 对象。
    
    该函数使用 Turf.js 库的 transformRotate 方法，围绕质心或指定枢轴点旋转 GeoJSON 对象。
    
    Args:
        geojson: GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0,29],[3.5,29],[2.5,32],[0,29]]]}}'
        
        angle: 旋转角度
            - 类型: float
            - 描述: 旋转角度（十进制度数），顺时针为正
            - 示例: 10.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - pivot: 旋转枢轴点坐标 (默认: 'centroid')
                - mutate: 是否允许修改输入对象 (默认: false)
            - 示例: '{"pivot": [0, 25], "mutate": false}'
    
    Returns:
        str: JSON 字符串格式的旋转后的 GeoJSON 对象
            - 类型: 与输入相同的 GeoJSON 类型
            - 格式: 与输入相同的格式
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0.5,29.2],[3.8,29.1],[2.7,32.3],[0.5,29.2]]]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson = '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0,29],[3.5,29],[2.5,32],[0,29]]]}}'
        >>> options = '{"pivot": [0, 25]}'
        >>> result = asyncio.run(transformRotate(geojson, 10.0, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0.5,29.2],[3.8,29.1],[2.7,32.3],[0.5,29.2]]]}}'
    
    Notes:
        - 输入参数 geojson 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 角度为十进制度数，顺时针为正
        - 默认围绕几何图形的质心旋转
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const angle = parseFloat({angle});
        const options = JSON.parse('{options_param}');
        const result = turf.transformRotate(geojson, angle, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def transformTranslate(geojson: str, distance: float, direction: float, options: str = None) -> str:
    """
    平移 GeoJSON 对象。
    
    该函数使用 Turf.js 库的 transformTranslate 方法，沿恒向线移动 GeoJSON 对象。
    
    Args:
        geojson: GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0,29],[3.5,29],[2.5,32],[0,29]]]}}'
        
        distance: 移动距离
            - 类型: float
            - 描述: 移动距离，负值表示相反方向
            - 示例: 100.0
        
        direction: 移动方向
            - 类型: float
            - 描述: 移动方向（十进制度数），从北方向顺时针测量
            - 示例: 35.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
                - zTranslation: 垂直移动距离 (默认: 0)
                - mutate: 是否允许修改输入对象 (默认: false)
            - 示例: '{"units": "miles", "zTranslation": 10, "mutate": false}'
    
    Returns:
        str: JSON 字符串格式的平移后的 GeoJSON 对象
            - 类型: 与输入相同的 GeoJSON 类型
            - 格式: 与输入相同的格式
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0.6,29.3],[4.1,29.3],[3.1,32.3],[0.6,29.3]]]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson = '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0,29],[3.5,29],[2.5,32],[0,29]]]}}'
        >>> options = '{"units": "miles"}'
        >>> result = asyncio.run(transformTranslate(geojson, 100.0, 35.0, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0.6,29.3],[4.1,29.3],[3.1,32.3],[0.6,29.3]]]}}'
    
    Notes:
        - 输入参数 geojson 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 方向从北方向顺时针测量
        - 距离可以为负值，表示相反方向移动
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const distance = parseFloat({distance});
        const direction = parseFloat({direction});
        const options = JSON.parse('{options_param}');
        const result = turf.transformTranslate(geojson, distance, direction, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def transformScale(geojson: str, factor: float, options: str = None) -> str:
    """
    缩放 GeoJSON 对象。
    
    该函数使用 Turf.js 库的 transformScale 方法，从给定点缩放 GeoJSON 对象。
    
    Args:
        geojson: GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0,29],[3.5,29],[2.5,32],[0,29]]]}}'
        
        factor: 缩放因子
            - 类型: float
            - 描述: 缩放因子，例如 2 表示放大两倍
            - 示例: 3.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - origin: 缩放原点坐标 (默认: 'centroid')
                - mutate: 是否允许修改输入对象 (默认: false)
            - 示例: '{"origin": [0, 25], "mutate": false}'
    
    Returns:
        str: JSON 字符串格式的缩放后的 GeoJSON 对象
            - 类型: 与输入相同的 GeoJSON 类型
            - 格式: 与输入相同的格式
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0,29],[10.5,29],[7.5,32],[0,29]]]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson = '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0,29],[3.5,29],[2.5,32],[0,29]]]}}'
        >>> result = asyncio.run(transformScale(geojson, 3.0))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0,29],[10.5,29],[7.5,32],[0,29]]]}}'
    
    Notes:
        - 输入参数 geojson 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 缩放因子为 2 表示尺寸加倍
        - 默认从几何图形的质心缩放
        - 对于 FeatureCollection，为每个特征单独计算原点
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const factor = parseFloat({factor});
        const options = JSON.parse('{options_param}');
        const result = turf.transformScale(geojson, factor, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def union(featureCollection: str) -> str:
    """
    合并两个多边形。
    
    该函数使用 Turf.js 库的 union 方法，合并两个多边形为一个多边形。
    
    Args:
        featureCollection: 包含两个多边形的 GeoJSON FeatureCollection
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON FeatureCollection 规范，包含两个 Polygon 特征
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-82.574787, 35.594087], [-82.574787, 35.615581], [-82.545261, 35.615581], [-82.545261, 35.594087], [-82.574787, 35.594087]]]}}, {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-82.560024, 35.585153], [-82.560024, 35.602602], [-82.52964, 35.602602], [-82.52964, 35.585153], [-82.560024, 35.585153]]]}}]}'
    
    Returns:
        str: JSON 字符串格式的合并后的 GeoJSON Feature
            - 类型: GeoJSON Feature with Polygon or MultiPolygon geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-82.574787, 35.585153], [-82.574787, 35.615581], [-82.52964, 35.615581], [-82.52964, 35.585153], [-82.574787, 35.585153]]]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> featureCollection = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-82.574787, 35.594087], [-82.574787, 35.615581], [-82.545261, 35.615581], [-82.545261, 35.594087], [-82.574787, 35.594087]]]}}, {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-82.560024, 35.585153], [-82.560024, 35.602602], [-82.52964, 35.602602], [-82.52964, 35.585153], [-82.560024, 35.585153]]]}}]}'
        >>> result = asyncio.run(union(featureCollection))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-82.574787, 35.585153], [-82.574787, 35.615581], [-82.52964, 35.615581], [-82.52964, 35.585153], [-82.574787, 35.585153]]]}}'
    
    Notes:
        - 输入参数 featureCollection 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 合并两个多边形的几何并集
        - 返回包含两个多边形所有区域的多边形
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const featureCollection = JSON.parse('{featureCollection}');
        const result = turf.union(featureCollection);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def buffer(geojson: str, radius: float, options: str = None) -> str:
    """
    为 GeoJSON 特征创建缓冲区。
    
    此功能为输入的 GeoJSON 特征创建指定半径的缓冲区多边形。
    
    Args:
        geojson: GeoJSON 特征
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-90.548630, 14.616599]}}'
        
        radius: 缓冲区半径
            - 类型: float
            - 描述: 缓冲区的半径值
            - 示例: 500.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
                - steps: 缓冲区边界分段数 (默认: 64)
            - 示例: '{"units": "miles", "steps": 32}'
    
    Returns:
        str: JSON 字符串格式的缓冲区 GeoJSON Polygon 特征
            - 类型: GeoJSON Feature with Polygon geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-90.55, 14.62], ...]]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson = '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-90.548630, 14.616599]}}'
        >>> options = '{"units": "miles"}'
        >>> result = asyncio.run(buffer(geojson, 500.0, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-90.55, 14.62], ...]]}}'
    
    Notes:
        - 输入参数 geojson 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 可以为点、线、多边形等几何类型创建缓冲区
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const radius = parseFloat({radius});
        const options = JSON.parse('{options_param}');
        const result = turf.buffer(geojson, radius, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@transformation_mcp.tool
async def voronoi(points: str, options: str = None) -> str:
    """
    生成 Voronoi 多边形。
    
    该函数使用 Turf.js 库的 voronoi 方法，从点集生成 Voronoi 多边形。
    
    Args:
        points: 点集 GeoJSON FeatureCollection
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON FeatureCollection 规范，包含 Point 特征
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, ...]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - bbox: 裁剪矩形边界框 (默认: [-180,-85,180,-85])
            - 示例: '{"bbox": [-70, 40, -60, 60]}'
    
    Returns:
        str: JSON 字符串格式的 Voronoi 多边形集合 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Polygon features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-75.35, 39.98], [-75.34, 39.99], ...]]}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> points = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}]}'
        >>> options = '{"bbox": [-70, 40, -60, 60]}'
        >>> result = asyncio.run(voronoi(points, options))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-75.35, 39.98], [-75.34, 39.99], ...]]}}, ...]}'
    
    Notes:
        - 输入参数 points 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 算法来自 d3-voronoi 包
        - 每个输入点对应一个输出多边形
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const points = JSON.parse('{points}');
        const options = JSON.parse('{options_param}');
        const result = turf.voronoi(points, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")
