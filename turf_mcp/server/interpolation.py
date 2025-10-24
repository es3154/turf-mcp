# 空间插值和表面分析函数

from fastmcp import FastMCP

from turf_mcp.utils import call_js_script

interpolation_mcp = FastMCP("interpolation")

@interpolation_mcp.tool
async def interpolate(points: str, cell_size: float, options: str = None) -> str:
    """
    使用反距离权重法进行空间插值。
    
    此功能根据已知点的属性值，使用反距离权重法在网格上估计属性值。
    
    Args:
        points: 已知点的特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON FeatureCollection)
            - 格式: FeatureCollection with Point features
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984], "properties": {"elevation": 100}}, ...]}'
        
        cell_size: 网格单元大小
            - 类型: float
            - 描述: 每个网格单元的距离
            - 示例: 100.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - gridType: 网格类型 ('square', 'point', 'hex', 'triangle') (默认: 'square')
                - property: 用于插值的属性名 (默认: 'elevation')
                - units: 距离单位 (默认: 'kilometers')
                - weight: 距离衰减权重指数 (默认: 1)
                - bbox: 边界框数组 [minX, minY, maxX, maxY]
            - 示例: '{"gridType": "point", "property": "temperature", "units": "miles"}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Point or Polygon features
            - 格式: {"type": "FeatureCollection", "features": [...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984], "properties": {"temperature": 25.5}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> points = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984], "properties": {"temperature": 25.5}}]}'
        >>> result = asyncio.run(interpolate(points, 100.0, '{"gridType": "point", "property": "temperature"}'))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984], "properties": {"temperature": 25.5}}, ...]}'
    
    Notes:
        - 输入参数 points 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 反距离权重法假设距离越近的点对插值结果影响越大
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const points = JSON.parse('{points}');
        const cellSize = parseFloat({cell_size});
        const options = JSON.parse('{options_param}');
        const result = turf.interpolate(points, cellSize, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@interpolation_mcp.tool
async def isobands(point_grid: str, breaks: str, options: str = None) -> str:
    """
    从点网格生成等值带。
    
    此功能从具有z值的点网格生成填充的等值带，用于创建连续值的区域表示。
    
    Args:
        point_grid: 点网格特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON FeatureCollection)
            - 格式: FeatureCollection with Point features (必须是方形或矩形网格)
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984], "properties": {"elevation": 100}}, ...]}'
        
        breaks: 等值带断点数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: [break1, break2, break3, ...]
            - 示例: '[0, 10, 20, 30, 40]'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - zProperty: z值属性名 (默认: 'elevation')
                - commonProperties: 传递给所有等值带的属性对象
                - breaksProperties: 按顺序传递给对应等值带的属性对象数组
            - 示例: '{"zProperty": "temperature", "commonProperties": {"type": "isoband"}}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with MultiPolygon features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "MultiPolygon", "coordinates": [...]}, "properties": {...}}, ...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "MultiPolygon", "coordinates": [...]}, "properties": {"min": 0, "max": 10}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> point_grid = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984], "properties": {"temperature": 25.5}}]}'
        >>> breaks = '[0, 10, 20, 30]'
        >>> result = asyncio.run(isobands(point_grid, breaks, '{"zProperty": "temperature"}'))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "MultiPolygon", "coordinates": [...]}, "properties": {"min": 0, "max": 10}}, ...]}'
    
    Notes:
        - 输入参数 point_grid、breaks 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 点网格必须是方形或矩形排列
        - 等值带用于可视化连续数据的范围
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const pointGrid = JSON.parse('{point_grid}');
        const breaks = JSON.parse('{breaks}');
        const options = JSON.parse('{options_param}');
        const result = turf.isobands(pointGrid, breaks, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@interpolation_mcp.tool
async def isolines(point_grid: str, breaks: str, options: str = None) -> str:
    """
    从点网格生成等值线。
    
    此功能从具有z值的点网格生成等值线，用于创建连续值的线状表示。
    
    Args:
        point_grid: 点网格特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON FeatureCollection)
            - 格式: FeatureCollection with Point features (必须是方形或矩形网格)
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984], "properties": {"elevation": 100}}, ...]}'
        
        breaks: 等值线断点数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: [break1, break2, break3, ...]
            - 示例: '[0, 10, 20, 30, 40]'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - zProperty: z值属性名 (默认: 'elevation')
                - commonProperties: 传递给所有等值线的属性对象
                - breaksProperties: 按顺序传递给对应等值线的属性对象数组
            - 示例: '{"zProperty": "temperature", "commonProperties": {"type": "isolines"}}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with LineString features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}, "properties": {...}}, ...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}, "properties": {"value": 10}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> point_grid = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984], "properties": {"temperature": 25.5}}]}'
        >>> breaks = '[0, 10, 20, 30]'
        >>> result = asyncio.run(isolines(point_grid, breaks, '{"zProperty": "temperature"}'))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}, "properties": {"value": 10}}, ...]}'
    
    Notes:
        - 输入参数 point_grid、breaks 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 点网格必须是方形或矩形排列
        - 等值线用于可视化连续数据的等值边界
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const pointGrid = JSON.parse('{point_grid}');
        const breaks = JSON.parse('{breaks}');
        const options = JSON.parse('{options_param}');
        const result = turf.isolines(pointGrid, breaks, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@interpolation_mcp.tool
async def planepoint(point: str, triangle: str) -> str:
    """
    计算点在三角形平面上的z值。
    
    此功能根据三角形三个顶点的z值，计算给定点在三角形平面上的插值z值。
    
    Args:
        point: 点特征
            - 类型: str (JSON 字符串格式的 GeoJSON Feature)
            - 格式: Feature with Point geometry
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.3221, 39.529]}}'
        
        triangle: 三角形特征
            - 类型: str (JSON 字符串格式的 GeoJSON Feature)
            - 格式: Feature with Polygon geometry (必须包含三个顶点)
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-75.1221, 39.57], [-75.58, 39.18], [-75.97, 39.86], [-75.1221, 39.57]]]}, "properties": {"a": 11, "b": 122, "c": 44}}'
    
    Returns:
        str: JSON 字符串格式的z值结果
            - 类型: 包含 value 的对象
            - 格式: {"value": z值}
            - 示例: '{"value": 35.5}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> point = '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.3221, 39.529]}}'
        >>> triangle = '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-75.1221, 39.57], [-75.58, 39.18], [-75.97, 39.86], [-75.1221, 39.57]]]}, "properties": {"a": 11, "b": 122, "c": 44}}'
        >>> result = asyncio.run(planepoint(point, triangle))
        >>> print(result)
        '{"value": 35.5}'
    
    Notes:
        - 输入参数 point 和 triangle 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 三角形必须包含三个顶点，且首尾坐标相同形成闭合环
        - 三角形属性'a', 'b', 'c'分别对应三个顶点的z值
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const point = JSON.parse('{point}');
        const triangle = JSON.parse('{triangle}');
        const result = turf.planepoint(point, triangle);
        console.log(JSON.stringify({{"value": result}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@interpolation_mcp.tool
async def tin(points: str, z_property: str = None) -> str:
    """
    从点集创建不规则三角网。
    
    此功能从点集创建不规则三角网，用于表面建模和地形分析。
    
    Args:
        points: 点特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON FeatureCollection)
            - 格式: FeatureCollection with Point features
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984], "properties": {"elevation": 100}}, ...]}'
        
        z_property: z值属性名
            - 类型: str 或 None
            - 描述: 用于z值的属性名，如果为None则不添加额外数据
            - 示例: 'elevation'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Polygon features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}, "properties": {...}}, ...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}, "properties": {"a": 100, "b": 150, "c": 120}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> points = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984], "properties": {"elevation": 100}}]}'
        >>> result = asyncio.run(tin(points, 'elevation'))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}, "properties": {"a": 100, "b": 150, "c": 120}}, ...]}'
    
    Notes:
        - 输入参数 points 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 不规则三角网用于创建连续的表面模型
        - 每个三角形包含三个顶点的z值属性
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    z_property_param = f"'{z_property}'" if z_property else 'null'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const points = JSON.parse('{points}');
        const zProperty = {z_property_param};
        const result = turf.tin(points, zProperty);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")
