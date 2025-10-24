# 测量函数

from fastmcp import FastMCP

from turf_mcp.utils import call_js_script

measurement_mcp = FastMCP("measurement")

@measurement_mcp.tool
async def along(line: str, distance: float, options: str = None) -> str:
    """
    在线上计算指定距离处的点位置。
    
    此功能沿着给定线段从起点开始移动指定距离，找到对应的坐标点位置。
    
    Args:
        line: GeoJSON LineString 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON LineString 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[-83, 30], [-84, 36], [-78, 41]]}'
        
        distance: 沿线的距离
            - 类型: float
            - 描述: 从起点开始沿线的距离值
            - 范围: 0 到线的总长度（超出范围会自动截断到端点）
            - 示例: 200.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
                - 其他 Turf.js 支持的选项参数
            - 示例: '{"units": "miles"}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Point 特征
            - 类型: GeoJSON Feature with Point geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-82.5, 33.2]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> line = '{"type": "LineString", "coordinates": [[-83, 30], [-84, 36], [-78, 41]]}'
        >>> options = '{"units": "miles"}'
        >>> result = asyncio.run(along(line, 200, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-82.5, 33.2]}}'
    
    Notes:
        - 如果距离超过线长度，会自动返回线终点
        - 如果距离为负值，会自动返回线起点
        - 输入参数 line 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 依赖于 Turf.js 库和 Node.js 环境
    """


    js_script = f"""
        const turf = require('@turf/turf');
        const line = JSON.parse('{line}');
        const distance = parseFloat({distance});
        const options = JSON.parse('{options}');
        const result = turf.along(line, distance, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def area(polygon: str) -> str:
    """
    计算多边形区域的面积。
    
    此功能计算给定多边形区域的面积，返回以平方米为单位的数值结果。
    
    Args:
        polygon: GeoJSON 多边形特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Polygon 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Polygon", "coordinates": [[[125, -15], [113, -22], [154, -27], [144, -15], [125, -15]]]}'
    
    Returns:
        str: JSON 字符串格式的面积结果对象
            - 类型: 包含 value 和 units 的对象
            - 格式: {"value": 面积数值, "units": "square meters"}
            - 示例: '{"value": 1234567.89, "units": "square meters"}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> polygon = '{"type": "Polygon", "coordinates": [[[125, -15], [113, -22], [154, -27], [144, -15], [125, -15]]]}'
        >>> result = asyncio.run(area(polygon))
        >>> print(result)
        '{"value": 1234567.89, "units": "square meters"}'
    
    Notes:
        - 输入参数 polygon 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 返回的面积单位为平方米
        - 依赖于 Turf.js 库和 Node.js 环境
        - 支持 Polygon 和 MultiPolygon 几何类型
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const polygon = JSON.parse('{polygon}');
        const result = turf.area(polygon);
        console.log(JSON.stringify({{"value": result, "units": "square meters"}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def bbox(geojson: str) -> str:
    """
    计算地理对象的边界范围。
    
    此功能计算给定地理对象的边界框，返回包含对象的最小矩形范围坐标。
    
    Args:
        geojson: GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[-74, 40], [-78, 42], [-82, 35]]}'
    
    Returns:
        str: JSON 字符串格式的边界框数组
            - 类型: 数组 [minX, minY, maxX, maxY]
            - 格式: [最小经度, 最小纬度, 最大经度, 最大纬度]
            - 示例: '[-82, 35, -74, 42]'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> line = '{"type": "LineString", "coordinates": [[-74, 40], [-78, 42], [-82, 35]]}'
        >>> result = asyncio.run(bbox(line))
        >>> print(result)
        '[-82, 35, -74, 42]'
    
    Notes:
        - 输入参数 geojson 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 返回的边界框格式为 [minX, minY, maxX, maxY]
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const result = turf.bbox(geojson);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def bboxPolygon(bbox: str, options: str = None) -> str:
    """
    将边界框转换为多边形特征。
    
    此功能将边界框坐标转换为完整的多边形几何图形，便于进行多边形操作和可视化。
    
    Args:
        bbox: 边界框数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: [minX, minY, maxX, maxY]
            - 示例: '[-82, 35, -74, 42]'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - properties: 传递给多边形的属性对象
                - id: 传递给多边形的 ID
            - 示例: '{"properties": {"name": "bounding box"}, "id": "bbox1"}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Polygon 特征
            - 类型: GeoJSON Feature with Polygon geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-82, 35], [-74, 35], [-74, 42], [-82, 42], [-82, 35]]]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> bbox = '[-82, 35, -74, 42]'
        >>> options = '{"properties": {"name": "bounding box"}}'
        >>> result = asyncio.run(bboxPolygon(bbox, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-82, 35], [-74, 35], [-74, 42], [-82, 42], [-82, 35]]]}}'
    
    Notes:
        - 输入参数 bbox 和 options 必须是有效的 JSON 字符串
        - 边界框格式为 [minX, minY, maxX, maxY]
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const bbox = JSON.parse('{bbox}');
        const options = JSON.parse('{options_param}');
        const result = turf.bboxPolygon(bbox, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def bearing(point1: str, point2: str) -> str:
    """
    计算两点之间的地理方位角。
    
    该函数使用 Turf.js 库的 bearing 方法，计算从第一个点到第二个点的方位角。
    
    Args:
        point1: 起点 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        
        point2: 终点 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-75.534, 39.123]}'
    
    Returns:
        str: JSON 字符串格式的方位角结果对象
            - 类型: 包含 value 和 units 的对象
            - 格式: {"value": 方位角数值, "units": "degrees"}
            - 示例: '{"value": 45.5, "units": "degrees"}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> point1 = '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        >>> point2 = '{"type": "Point", "coordinates": [-75.534, 39.123]}'
        >>> result = asyncio.run(bearing(point1, point2))
        >>> print(result)
        '{"value": 45.5, "units": "degrees"}'
    
    Notes:
        - 输入参数 point1 和 point2 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 方位角是从北方向顺时针测量的角度
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const point1 = JSON.parse('{point1}');
        const point2 = JSON.parse('{point2}');
        const result = turf.bearing(point1, point2);
        console.log(JSON.stringify({{"value": result, "units": "degrees"}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def center(geojson: str, options: str = None) -> str:
    """
    计算特征集合的中心点。
    
    此功能计算给定特征集合的几何中心，返回所有特征边界框的中心点位置。
    
    Args:
        geojson: GeoJSON 特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON FeatureCollection 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-97.522259, 35.4691]}}, ...]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - properties: 传递给中心点的属性对象
                - bbox: 边界框数组
                - id: 传递给中心点的 ID
            - 示例: '{"properties": {"name": "center point"}}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Point 特征
            - 类型: GeoJSON Feature with Point geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-97.5, 35.5]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-97.522259, 35.4691]}}]}'
        >>> options = '{"properties": {"name": "center point"}}'
        >>> result = asyncio.run(center(geojson, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-97.5, 35.5]}}'
    
    Notes:
        - 输入参数 geojson 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 返回的中心点是所有特征边界框的中心
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const options = JSON.parse('{options_param}');
        const result = turf.center(geojson, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def centerOfMass(geojson: str, options: str = None) -> str:
    """
    计算 GeoJSON 对象的质心。
    
    该函数使用 Turf.js 库的 centerOfMass 方法，计算给定 GeoJSON 对象的质心。
    
    Args:
        geojson: GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Polygon", "coordinates": [[[-81, 41], [-88, 36], [-84, 31], [-80, 33], [-77, 39], [-81, 41]]]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - properties: 传递给质心的属性对象
            - 示例: '{"properties": {"name": "center of mass"}}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Point 特征
            - 类型: GeoJSON Feature with Point geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-82.5, 35.5]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> polygon = '{"type": "Polygon", "coordinates": [[[-81, 41], [-88, 36], [-84, 31], [-80, 33], [-77, 39], [-81, 41]]]}'
        >>> options = '{"properties": {"name": "center of mass"}}'
        >>> result = asyncio.run(centerOfMass(polygon, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-82.5, 35.5]}}'
    
    Notes:
        - 输入参数 geojson 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 质心是基于几何形状的质量分布计算的中心点
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const options = JSON.parse('{options_param}');
        const result = turf.centerOfMass(geojson, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def centroid(geojson: str, options: str = None) -> str:
    """
    计算几何对象的中心点。
    
    此功能计算给定几何对象的几何中心，通过平均所有顶点坐标确定中心位置。
    
    Args:
        geojson: GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Polygon", "coordinates": [[[-81, 41], [-88, 36], [-84, 31], [-80, 33], [-77, 39], [-81, 41]]]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - properties: 传递给几何中心的属性对象
            - 示例: '{"properties": {"name": "centroid"}}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Point 特征
            - 类型: GeoJSON Feature with Point geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-82.5, 35.5]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> polygon = '{"type": "Polygon", "coordinates": [[[-81, 41], [-88, 36], [-84, 31], [-80, 33], [-77, 39], [-81, 41]]]}'
        >>> options = '{"properties": {"name": "centroid"}}'
        >>> result = asyncio.run(centroid(polygon, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-82.5, 35.5]}}'
    
    Notes:
        - 输入参数 geojson 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 几何中心是通过平均所有顶点坐标计算的中心点
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const options = JSON.parse('{options_param}');
        const result = turf.centroid(geojson, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def destination(origin: str, distance: float, bearing: float, options: str = None) -> str:
    """
    从起点计算指定距离和方位角的目标点。
    
    此功能从给定起点出发，沿着指定方位角移动指定距离，计算并返回目标点的位置坐标。
    
    Args:
        origin: 起点 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        
        distance: 移动距离
            - 类型: float
            - 描述: 从起点开始移动的距离值
            - 示例: 50.0
        
        bearing: 方位角
            - 类型: float
            - 描述: 从北方向顺时针测量的角度
            - 范围: -180 到 180 度
            - 示例: 90.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
                - properties: 传递给目标点的属性对象
            - 示例: '{"units": "miles", "properties": {"name": "destination"}}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Point 特征
            - 类型: GeoJSON Feature with Point geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-74.5, 39.5]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> origin = '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        >>> options = '{"units": "miles", "properties": {"name": "destination"}}'
        >>> result = asyncio.run(destination(origin, 50.0, 90.0, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-74.5, 39.5]}}'
    
    Notes:
        - 输入参数 origin 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 方位角是从北方向顺时针测量的角度
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const origin = JSON.parse('{origin}');
        const distance = parseFloat({distance});
        const bearing = parseFloat({bearing});
        const options = JSON.parse('{options_param}');
        const result = turf.destination(origin, distance, bearing, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def distance(point1: str, point2: str, options: str = None) -> str:
    """
    计算两点之间的球面距离。
    
    此功能计算地球上两点之间的实际距离，考虑地球曲率，返回指定单位的距离值。
    
    Args:
        point1: 第一个 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        
        point2: 第二个 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-75.534, 39.123]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
            - 示例: '{"units": "miles"}'
    
    Returns:
        str: JSON 字符串格式的距离结果对象
            - 类型: 包含 value 和 units 的对象
            - 格式: {"value": 距离数值, "units": "距离单位"}
            - 示例: '{"value": 123.45, "units": "miles"}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> point1 = '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        >>> point2 = '{"type": "Point", "coordinates": [-75.534, 39.123]}'
        >>> options = '{"units": "miles"}'
        >>> result = asyncio.run(distance(point1, point2, options))
        >>> print(result)
        '{"value": 123.45, "units": "miles"}'
    
    Notes:
        - 输入参数 point1、point2 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 计算的是两点之间的球面距离
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const point1 = JSON.parse('{point1}');
        const point2 = JSON.parse('{point2}');
        const options = JSON.parse('{options_param}');
        const units = options && options.units ? options.units : 'kilometers';
        const result = turf.distance(point1, point2, options);
        console.log(JSON.stringify({{"value": result, "units": units}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def envelope(geojson: str) -> str:
    """
    将地理对象转换为边界框多边形。
    
    此功能计算给定地理对象的边界框，并将其转换为完整的多边形几何图形，便于进行多边形操作。
    
    Args:
        geojson: GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, ...]}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Polygon 特征
            - 类型: GeoJSON Feature with Polygon geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-82, 35], [-74, 35], [-74, 42], [-82, 42], [-82, 35]]]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}]}'
        >>> result = asyncio.run(envelope(geojson))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-82, 35], [-74, 35], [-74, 42], [-82, 42], [-82, 35]]]}}'
    
    Notes:
        - 输入参数 geojson 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 包络多边形是包含所有输入特征的最小边界框多边形
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const result = turf.envelope(geojson);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def length(geojson: str, options: str = None) -> str:
    """
    计算线或多线的长度。
    
    此功能计算给定线或多线几何图形的实际长度，考虑地球曲率，返回指定单位的长度值。
    
    Args:
        geojson: GeoJSON 线或多线对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON LineString 或 MultiLineString 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[-74, 40], [-78, 42], [-82, 35]]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
            - 示例: '{"units": "miles"}'
    
    Returns:
        str: JSON 字符串格式的长度结果对象
            - 类型: 包含 value 和 units 的对象
            - 格式: {"value": 长度数值, "units": "距离单位"}
            - 示例: '{"value": 123.45, "units": "miles"}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> line = '{"type": "LineString", "coordinates": [[-74, 40], [-78, 42], [-82, 35]]}'
        >>> options = '{"units": "miles"}'
        >>> result = asyncio.run(length(line, options))
        >>> print(result)
        '123.45'
    
    Notes:
        - 输入参数 geojson 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 计算的是线或多线的球面长度
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const options = JSON.parse('{options_param}');
        const units = options && options.units ? options.units : 'kilometers';
        const result = turf.length(geojson, options);
        console.log(JSON.stringify({{"value": result, "units": units}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def midpoint(point1: str, point2: str) -> str:
    """
    计算两点之间的中点。
    
    该函数使用 Turf.js 库的 midpoint 方法，计算两个 GeoJSON 点特征之间的中点。
    
    Args:
        point1: 第一个 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [144.834823, -37.771257]}'
        
        point2: 第二个 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [145.14244, -37.830937]}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Point 特征
            - 类型: GeoJSON Feature with Point geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [144.9886315, -37.801097]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> point1 = '{"type": "Point", "coordinates": [144.834823, -37.771257]}'
        >>> point2 = '{"type": "Point", "coordinates": [145.14244, -37.830937]}'
        >>> result = asyncio.run(midpoint(point1, point2))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [144.9886315, -37.801097]}}'
    
    Notes:
        - 输入参数 point1 和 point2 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 计算的是两点之间的球面中点
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const point1 = JSON.parse('{point1}');
        const point2 = JSON.parse('{point2}');
        const result = turf.midpoint(point1, point2);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def pointOnFeature(geojson: str) -> str:
    """
    在 GeoJSON 特征上找到最近的点。
    
    该函数使用 Turf.js 库的 pointOnFeature 方法，在给定的 GeoJSON 特征上找到最近的点。
    
    Args:
        geojson: GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Polygon", "coordinates": [[[-81, 41], [-88, 36], [-84, 31], [-80, 33], [-77, 39], [-81, 41]]]}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Point 特征
            - 类型: GeoJSON Feature with Point geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-82.5, 35.5]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> polygon = '{"type": "Polygon", "coordinates": [[[-81, 41], [-88, 36], [-84, 31], [-80, 33], [-77, 39], [-81, 41]]]}'
        >>> result = asyncio.run(pointOnFeature(polygon))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-82.5, 35.5]}}'
    
    Notes:
        - 输入参数 geojson 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 返回的特征上最近的点
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const result = turf.pointOnFeature(geojson);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def pointToLineDistance(point: str, line: str, options: str = None) -> str:
    """
    计算点到线的最短距离。
    
    该函数使用 Turf.js 库的 pointToLineDistance 方法，计算点到线的最短距离。
    
    Args:
        point: 点 GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        
        line: 线 GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON LineString 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[-74, 40], [-78, 42], [-82, 35]]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
                - method: 计算方法 (默认: 'geodesic')
                    - 有效值: 'geodesic', 'planar'
            - 示例: '{"units": "miles", "method": "geodesic"}'
    
    Returns:
        str: JSON 字符串格式的距离结果对象
            - 类型: 包含 value 和 units 的对象
            - 格式: {"value": 距离数值, "units": "距离单位"}
            - 示例: '{"value": 12.34, "units": "miles"}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> point = '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        >>> line = '{"type": "LineString", "coordinates": [[-74, 40], [-78, 42], [-82, 35]]}'
        >>> options = '{"units": "miles", "method": "geodesic"}'
        >>> result = asyncio.run(pointToLineDistance(point, line, options))
        >>> print(result)
        '12.34'
    
    Notes:
        - 输入参数 point、line 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 计算的是点到线的最短球面距离
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const point = JSON.parse('{point}');
        const line = JSON.parse('{line}');
        const options = JSON.parse('{options_param}');
        const units = options && options.units ? options.units : 'kilometers';
        const result = turf.pointToLineDistance(point, line, options);
        console.log(JSON.stringify({{"value": result, "units": units}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def rhumbBearing(point1: str, point2: str, options: str = None) -> str:
    """
    计算两点之间的恒向线方位角。
    
    该函数使用 Turf.js 库的 rhumbBearing 方法，计算从第一个点到第二个点的恒向线方位角。
    
    Args:
        point1: 起点 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        
        point2: 终点 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-75.534, 39.123]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - final: 是否计算最终方位角 (默认: False)
            - 示例: '{"final": true}'
    
    Returns:
        str: JSON 字符串格式的方位角结果对象
            - 类型: 包含 value 和 units 的对象
            - 格式: {"value": 方位角数值, "units": "degrees"}
            - 示例: '{"value": 45.5, "units": "degrees"}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> point1 = '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        >>> point2 = '{"type": "Point", "coordinates": [-75.534, 39.123]}'
        >>> options = '{"final": true}'
        >>> result = asyncio.run(rhumbBearing(point1, point2, options))
        >>> print(result)
        '45.5'
    
    Notes:
        - 输入参数 point1、point2 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 恒向线方位角是沿着恒向线（等角航线）的方位角
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const point1 = JSON.parse('{point1}');
        const point2 = JSON.parse('{point2}');
        const options = JSON.parse('{options_param}');
        const result = turf.rhumbBearing(point1, point2, options);
        console.log(JSON.stringify({{"value": result, "units": "degrees"}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def rhumbDestination(origin: str, distance: float, bearing: float, options: str = None) -> str:
    """
    沿恒向线计算目标点。
    
    该函数使用 Turf.js 库的 rhumbDestination 方法，从起点沿着指定恒向线方位角移动指定距离来计算目标点。
    
    Args:
        origin: 起点 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        
        distance: 移动距离
            - 类型: float
            - 描述: 从起点开始移动的距离值
            - 示例: 50.0
        
        bearing: 恒向线方位角
            - 类型: float
            - 描述: 从北方向顺时针测量的恒向线角度
            - 范围: -180 到 180 度
            - 示例: 90.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
                - properties: 传递给目标点的属性对象
            - 示例: '{"units": "miles", "properties": {"name": "rhumb destination"}}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Point 特征
            - 类型: GeoJSON Feature with Point geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-74.5, 39.5]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> origin = '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        >>> options = '{"units": "miles", "properties": {"name": "rhumb destination"}}'
        >>> result = asyncio.run(rhumbDestination(origin, 50.0, 90.0, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-74.5, 39.5]}}'
    
    Notes:
        - 输入参数 origin 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 恒向线方位角是沿着恒向线（等角航线）的方位角
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const origin = JSON.parse('{origin}');
        const distance = parseFloat({distance});
        const bearing = parseFloat({bearing});
        const options = JSON.parse('{options_param}');
        const result = turf.rhumbDestination(origin, distance, bearing, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def rhumbDistance(point1: str, point2: str, options: str = None) -> str:
    """
    计算两点之间的恒向线距离。
    
    该函数使用 Turf.js 库的 rhumbDistance 方法，计算两个 GeoJSON 点特征之间的恒向线距离。
    
    Args:
        point1: 第一个 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        
        point2: 第二个 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-75.534, 39.123]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
            - 示例: '{"units": "miles"}'
    
    Returns:
        str: JSON 字符串格式的距离结果对象
            - 类型: 包含 value 和 units 的对象
            - 格式: {"value": 距离数值, "units": "距离单位"}
            - 示例: '{"value": 123.45, "units": "miles"}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> point1 = '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        >>> point2 = '{"type": "Point", "coordinates": [-75.534, 39.123]}'
        >>> options = '{"units": "miles"}'
        >>> result = asyncio.run(rhumbDistance(point1, point2, options))
        >>> print(result)
        '123.45'
    
    Notes:
        - 输入参数 point1、point2 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 计算的是两点之间的恒向线距离（等角航线距离）
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const point1 = JSON.parse('{point1}');
        const point2 = JSON.parse('{point2}');
        const options = JSON.parse('{options_param}');
        const units = options && options.units ? options.units : 'kilometers';
        const result = turf.rhumbDistance(point1, point2, options);
        console.log(JSON.stringify({{"value": result, "units": units}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def square(bbox: str) -> str:
    """
    计算包含边界框的最小正方形边界框。
    
    该函数使用 Turf.js 库的 square 方法，计算包含给定边界框的最小正方形边界框。
    
    Args:
        bbox: 边界框数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: [minX, minY, maxX, maxY]
            - 示例: '[-20, -20, -15, 0]'
    
    Returns:
        str: JSON 字符串格式的正方形边界框数组
            - 类型: 数组 [minX, minY, maxX, maxY]
            - 格式: [最小经度, 最小纬度, 最大经度, 最大纬度]
            - 示例: '[-20, -20, 0, 0]'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> bbox = '[-20, -20, -15, 0]'
        >>> result = asyncio.run(square(bbox))
        >>> print(result)
        '[-20, -20, 0, 0]'
    
    Notes:
        - 输入参数 bbox 必须是有效的 JSON 字符串
        - 边界框格式为 [minX, minY, maxX, maxY]
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 返回的是包含输入边界框的最小正方形边界框
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const bbox = JSON.parse('{bbox}');
        const result = turf.square(bbox);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def greatCircle(start: str, end: str, options: str = None) -> str:
    """
    计算两点之间的大圆路径。
    
    该函数使用 Turf.js 库的 greatCircle 方法，计算两个 GeoJSON 点特征之间的大圆路径。
    
    Args:
        start: 起点 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-122, 48]}'
        
        end: 终点 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-77, 39]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - properties: 传递给大圆路径的属性对象
                - npoints: 路径上的点数 (默认: 100)
                - offset: 控制跨越日期变更线时路径分割的可能性 (默认: 10)
            - 示例: '{"properties": {"name": "Seattle to DC"}, "npoints": 200}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON LineString 或 MultiLineString 特征
            - 类型: GeoJSON Feature with LineString or MultiLineString geometry
            - 格式: {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}} 或 {"type": "Feature", "geometry": {"type": "MultiLineString", "coordinates": [...]}}
            - 示例: '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-122, 48], [-120, 47], ...]}}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> start = '{"type": "Point", "coordinates": [-122, 48]}'
        >>> end = '{"type": "Point", "coordinates": [-77, 39]}'
        >>> options = '{"properties": {"name": "Seattle to DC"}, "npoints": 200}'
        >>> result = asyncio.run(greatCircle(start, end, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-122, 48], [-120, 47], ...]}}'
    
    Notes:
        - 输入参数 start、end 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 如果起点和终点跨越日期变更线，结果可能是 MultiLineString
        - 大圆路径是球面上两点之间的最短路径
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const start = JSON.parse('{start}');
        const end = JSON.parse('{end}');
        const options = JSON.parse('{options_param}');
        const result = turf.greatCircle(start, end, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@measurement_mcp.tool
async def polygonTangents(point: str, polygon: str) -> str:
    """
    计算多边形上的切线点。
    
    该函数使用 Turf.js 库的 polygonTangents 方法，计算从给定点到多边形（或多边形集合）的两个切线点。
    
    Args:
        point: 点 GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [61, 5]}'
        
        polygon: 多边形 GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Polygon 或 MultiPolygon 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Polygon", "coordinates": [[[11, 0], [22, 4], [31, 0], [31, 11], [21, 15], [11, 11], [11, 0]]]}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Point features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng1, lat1]}}, {"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng2, lat2]}}]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [15, 8]}}, {"type": "Feature", "geometry": {"type": "Point", "coordinates": [25, 3]}}]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> point = '{"type": "Point", "coordinates": [61, 5]}'
        >>> polygon = '{"type": "Polygon", "coordinates": [[[11, 0], [22, 4], [31, 0], [31, 11], [21, 15], [11, 11], [11, 0]]]}'
        >>> result = asyncio.run(polygonTangents(point, polygon))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [15, 8]}}, {"type": "Feature", "geometry": {"type": "Point", "coordinates": [25, 3]}}]}'
    
    Notes:
        - 输入参数 point 和 polygon 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 返回两个切线点，分别对应多边形的两个切线
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const point = JSON.parse('{point}');
        const polygon = JSON.parse('{polygon}');
        const result = turf.polygonTangents(point, polygon);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")
