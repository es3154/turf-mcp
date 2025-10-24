# 杂项地理操作函数

from fastmcp import FastMCP

from turf_mcp.utils import call_js_script

misc_mcp = FastMCP("misc")

@misc_mcp.tool
async def kinks(geojson: str) -> str:
    """
    查找几何图形中的自相交点。
    
    此功能检测线或多边形几何图形中的自相交点（扭结点），返回这些交叉点的位置坐标。
    
    Args:
        geojson: GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 支持 LineString、MultiLineString、Polygon、MultiPolygon
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Polygon", "coordinates": [[[-12.034835, 8.901183], [-12.060413, 8.899826], [-12.03638, 8.873199], [-12.059383, 8.871418], [-12.034835, 8.901183]]]}'
    
    Returns:
        str: JSON 字符串格式的点特征集合
            - 类型: GeoJSON FeatureCollection with Point features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}}, ...]}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> polygon = '{"type": "Polygon", "coordinates": [[[-12.034835, 8.901183], [-12.060413, 8.899826], [-12.03638, 8.873199], [-12.059383, 8.871418], [-12.034835, 8.901183]]]}'
        >>> result = asyncio.run(kinks(polygon))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-12.045, 8.885]}}]}'
    
    Notes:
        - 输入参数 geojson 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 返回所有自相交点的位置坐标
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const result = turf.kinks(geojson);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@misc_mcp.tool
async def line_arc(center: str, radius: float, bearing1: float, bearing2: float, options: str = None) -> str:
    """
    创建圆弧线段。
    
    此功能以给定点为中心，创建指定半径和方位角范围的圆弧线段。
    
    Args:
        center: 中心点 GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-75, 40]}'
        
        radius: 圆弧半径
            - 类型: float
            - 描述: 圆弧的半径值
            - 示例: 5.0
        
        bearing1: 起始方位角
            - 类型: float
            - 描述: 圆弧起始方位角（从北方向顺时针测量）
            - 示例: 25.0
        
        bearing2: 结束方位角
            - 类型: float
            - 描述: 圆弧结束方位角（从北方向顺时针测量）
            - 示例: 45.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
                - steps: 圆弧分段数 (默认: 64)
                - properties: 传递给圆弧线的属性对象
            - 示例: '{"units": "miles", "steps": 32}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON LineString 特征
            - 类型: GeoJSON Feature with LineString geometry
            - 格式: {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> center = '{"type": "Point", "coordinates": [-75, 40]}'
        >>> options = '{"units": "miles", "steps": 32}'
        >>> result = asyncio.run(line_arc(center, 5.0, 25.0, 45.0, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-75, 40], ...]}}'
    
    Notes:
        - 输入参数 center 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 方位角是从北方向顺时针测量的角度
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const center = JSON.parse('{center}');
        const radius = parseFloat({radius});
        const bearing1 = parseFloat({bearing1});
        const bearing2 = parseFloat({bearing2});
        const options = JSON.parse('{options_param}');
        const result = turf.lineArc(center, radius, bearing1, bearing2, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@misc_mcp.tool
async def line_chunk(geojson: str, segment_length: float, options: str = None) -> str:
    """
    将线分割为指定长度的线段。
    
    此功能将线或多线几何图形分割为多个指定长度的线段，便于分段处理和分析。
    
    Args:
        geojson: GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON FeatureCollection, Geometry 或 Feature 规范，包含 LineString 或 MultiLineString
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[-95, 40], [-93, 45], [-85, 50]]}'
        
        segment_length: 线段长度
            - 类型: float
            - 描述: 每个线段的长度值
            - 示例: 15.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
                - reverse: 是否反转坐标顺序 (默认: false)
            - 示例: '{"units": "miles", "reverse": false}'
    
    Returns:
        str: JSON 字符串格式的线特征集合
            - 类型: GeoJSON FeatureCollection with LineString features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}}, ...]}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> line = '{"type": "LineString", "coordinates": [[-95, 40], [-93, 45], [-85, 50]]}'
        >>> options = '{"units": "miles"}'
        >>> result = asyncio.run(line_chunk(line, 15.0, options))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}}, ...]}'
    
    Notes:
        - 输入参数 geojson 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 如果线长度小于分段长度，则返回原始线
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const segmentLength = parseFloat({segment_length});
        const options = JSON.parse('{options_param}');
        const result = turf.lineChunk(geojson, segmentLength, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@misc_mcp.tool
async def line_intersect(line1: str, line2: str, options: str = None) -> str:
    """
    计算两条线的交点。
    
    此功能计算两条线或多边形几何图形之间的交点，返回所有交叉点的位置坐标。
    
    Args:
        line1: 第一条线 GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 支持 LineString、MultiLineString、Polygon、MultiPolygon
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[126, -11], [129, -21]]}'
        
        line2: 第二条线 GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 支持 LineString、MultiLineString、Polygon、MultiPolygon
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[123, -18], [131, -14]]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - removeDuplicates: 是否移除重复交点 (默认: true)
                - ignoreSelfIntersections: 是否忽略自相交点 (默认: true)
            - 示例: '{"removeDuplicates": true, "ignoreSelfIntersections": true}'
    
    Returns:
        str: JSON 字符串格式的点特征集合
            - 类型: GeoJSON FeatureCollection with Point features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}}, ...]}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> line1 = '{"type": "LineString", "coordinates": [[126, -11], [129, -21]]}'
        >>> line2 = '{"type": "LineString", "coordinates": [[123, -18], [131, -14]]}'
        >>> result = asyncio.run(line_intersect(line1, line2))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [127.5, -16]}}]}'
    
    Notes:
        - 输入参数 line1 和 line2 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 返回两条线之间的所有交点
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const line1 = JSON.parse('{line1}');
        const line2 = JSON.parse('{line2}');
        const options = JSON.parse('{options_param}');
        const result = turf.lineIntersect(line1, line2, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@misc_mcp.tool
async def line_overlap(line1: str, line2: str, options: str = None) -> str:
    """
    查找两条线的重叠部分。
    
    此功能计算两条线几何图形之间的重叠线段，返回这些重叠部分的几何图形。
    
    Args:
        line1: 第一条线 GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 支持 LineString、MultiLineString、Polygon、MultiPolygon
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[115, -35], [125, -30], [135, -30], [145, -35]]}'
        
        line2: 第二条线 GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 支持 LineString、MultiLineString、Polygon、MultiPolygon
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[115, -25], [125, -30], [135, -30], [145, -25]]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - tolerance: 容差距离
            - 示例: '{"tolerance": 0.01}'
    
    Returns:
        str: JSON 字符串格式的线特征集合
            - 类型: GeoJSON FeatureCollection with LineString features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}}, ...]}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> line1 = '{"type": "LineString", "coordinates": [[115, -35], [125, -30], [135, -30], [145, -35]]}'
        >>> line2 = '{"type": "LineString", "coordinates": [[115, -25], [125, -30], [135, -30], [145, -25]]}'
        >>> result = asyncio.run(line_overlap(line1, line2))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[125, -30], [135, -30]]}}]}'
    
    Notes:
        - 输入参数 line1 和 line2 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 返回两条线之间的所有重叠线段
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const line1 = JSON.parse('{line1}');
        const line2 = JSON.parse('{line2}');
        const options = JSON.parse('{options_param}');
        const result = turf.lineOverlap(line1, line2, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@misc_mcp.tool
async def line_segment(geojson: str) -> str:
    """
    将几何图形分解为线段。
    
    此功能将线或多边形几何图形分解为独立的线段，每个线段包含两个顶点坐标。
    
    Args:
        geojson: GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 支持 LineString、MultiLineString、Polygon、MultiPolygon
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Polygon", "coordinates": [[[-50, 5], [-40, -10], [-50, -10], [-40, 5], [-50, 5]]]}'
    
    Returns:
        str: JSON 字符串格式的线特征集合
            - 类型: GeoJSON FeatureCollection with LineString features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}}, ...]}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> polygon = '{"type": "Polygon", "coordinates": [[[-50, 5], [-40, -10], [-50, -10], [-40, 5], [-50, 5]]]}'
        >>> result = asyncio.run(line_segment(polygon))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-50, 5], [-40, -10]]}}, ...]}'
    
    Notes:
        - 输入参数 geojson 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 返回所有几何图形的独立线段
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const result = turf.lineSegment(geojson);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@misc_mcp.tool
async def line_slice(start_point: str, end_point: str, line: str) -> str:
    """
    在线段上截取指定起点和终点之间的部分。
    
    此功能在线段上找到与起点和终点最近的位置，并截取这两点之间的线段部分。
    
    Args:
        start_point: 起点 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-77.029609, 38.881946]}'
        
        end_point: 终点 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-77.021884, 38.889563]}'
        
        line: 线 GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON LineString 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[-77.031669, 38.878605], [-77.029609, 38.881946], [-77.020339, 38.884084], [-77.025661, 38.885821], [-77.021884, 38.889563], [-77.019824, 38.892368]]}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON LineString 特征
            - 类型: GeoJSON Feature with LineString geometry
            - 格式: {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> start = '{"type": "Point", "coordinates": [-77.029609, 38.881946]}'
        >>> end = '{"type": "Point", "coordinates": [-77.021884, 38.889563]}'
        >>> line = '{"type": "LineString", "coordinates": [[-77.031669, 38.878605], [-77.029609, 38.881946], [-77.020339, 38.884084], [-77.025661, 38.885821], [-77.021884, 38.889563], [-77.019824, 38.892368]]}'
        >>> result = asyncio.run(line_slice(start, end, line))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-77.029609, 38.881946], [-77.021884, 38.889563]]}}'
    
    Notes:
        - 输入参数 start_point、end_point 和 line 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 截取起点和终点之间的线段部分
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const startPoint = JSON.parse('{start_point}');
        const endPoint = JSON.parse('{end_point}');
        const line = JSON.parse('{line}');
        const result = turf.lineSlice(startPoint, endPoint, line);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@misc_mcp.tool
async def line_slice_along(line: str, start_distance: float, stop_distance: float, options: str = None) -> str:
    """
    沿线段长度截取指定距离范围的部分。
    
    此功能根据起点距离和终点距离在线段上截取对应的部分，便于按长度分割线段。
    
    Args:
        line: 线 GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON LineString 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[7, 45], [9, 45], [14, 40], [14, 41]]}'
        
        start_distance: 起点距离
            - 类型: float
            - 描述: 从线段起点开始的截取起始距离
            - 示例: 12.5
        
        stop_distance: 终点距离
            - 类型: float
            - 描述: 从线段起点开始的截取结束距离
            - 示例: 25.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
            - 示例: '{"units": "miles"}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON LineString 特征
            - 类型: GeoJSON Feature with LineString geometry
            - 格式: {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> line = '{"type": "LineString", "coordinates": [[7, 45], [9, 45], [14, 40], [14, 41]]}'
        >>> options = '{"units": "miles"}'
        >>> result = asyncio.run(line_slice_along(line, 12.5, 25.0, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[...]]}}'
    
    Notes:
        - 输入参数 line 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 根据距离范围截取线段部分
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const line = JSON.parse('{line}');
        const startDistance = parseFloat({start_distance});
        const stopDistance = parseFloat({stop_distance});
        const options = JSON.parse('{options_param}');
        const result = turf.lineSliceAlong(line, startDistance, stopDistance, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@misc_mcp.tool
async def line_split(line: str, splitter: str) -> str:
    """
    用分割器将线段分割为多段。
    
    此功能使用分割器几何图形将线段分割为多个部分，返回分割后的线段集合。
    
    Args:
        line: 线 GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON LineString 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[120, -25], [145, -25]]}'
        
        splitter: 分割器 GeoJSON 特征
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 特征
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[130, -15], [130, -35]]}'
    
    Returns:
        str: JSON 字符串格式的线特征集合
            - 类型: GeoJSON FeatureCollection with LineString features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}}, ...]}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> line = '{"type": "LineString", "coordinates": [[120, -25], [145, -25]]}'
        >>> splitter = '{"type": "LineString", "coordinates": [[130, -15], [130, -35]]}'
        >>> result = asyncio.run(line_split(line, splitter))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[120, -25], [130, -25]]}}, {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[130, -25], [145, -25]]}}]}'
    
    Notes:
        - 输入参数 line 和 splitter 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 使用分割器将线段分割为多个部分
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const line = JSON.parse('{line}');
        const splitter = JSON.parse('{splitter}');
        const result = turf.lineSplit(line, splitter);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@misc_mcp.tool
async def mask(polygons: str, mask_polygon: str = None, options: str = None) -> str:
    """
    使用掩膜多边形裁剪几何图形。
    
    此功能使用掩膜多边形对输入多边形进行裁剪，返回掩膜范围内的多边形部分。
    
    Args:
        polygons: 输入多边形 GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 支持 Polygon、MultiPolygon、Feature<Polygon>、Feature<MultiPolygon>、FeatureCollection<Polygon | MultiPolygon>
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Polygon", "coordinates": [[[112, -21], [116, -36], [146, -39], [153, -24], [133, -10], [112, -21]]]}'
        
        mask_polygon: 掩膜多边形 GeoJSON 对象
            - 类型: str (JSON 字符串格式的 GeoJSON) 或 None
            - 格式: 支持 Polygon、Feature<Polygon>
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Polygon", "coordinates": [[[90, -55], [170, -55], [170, 10], [90, 10], [90, -55]]]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - mutate: 是否修改原始掩膜多边形 (默认: false)
            - 示例: '{"mutate": false}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Polygon 特征
            - 类型: GeoJSON Feature with Polygon geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> polygons = '{"type": "Polygon", "coordinates": [[[112, -21], [116, -36], [146, -39], [153, -24], [133, -10], [112, -21]]]}'
        >>> mask_polygon = '{"type": "Polygon", "coordinates": [[[90, -55], [170, -55], [170, 10], [90, 10], [90, -55]]]}'
        >>> result = asyncio.run(mask(polygons, mask_polygon))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}'
    
    Notes:
        - 输入参数 polygons 和 mask_polygon 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 如果未提供掩膜多边形，则使用世界范围作为掩膜
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    mask_param = mask_polygon if mask_polygon else 'null'
    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const polygons = JSON.parse('{polygons}');
        const maskPolygon = {mask_param} ? JSON.parse('{mask_polygon}') : undefined;
        const options = JSON.parse('{options_param}');
        const result = turf.mask(polygons, maskPolygon, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@misc_mcp.tool
async def nearest_point_on_line(line: str, point: str, options: str = None) -> str:
    """
    找到线上距离给定点最近的位置。
    
    此功能在线段上找到距离给定点最近的位置，返回该位置坐标及距离信息。
    
    Args:
        line: 线 GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON LineString 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "LineString", "coordinates": [[-77.031669, 38.878605], [-77.029609, 38.881946], [-77.020339, 38.884084], [-77.025661, 38.885821], [-77.021884, 38.889563], [-77.019824, 38.892368]]}'
        
        point: 点 GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-77.037076, 38.884017]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
            - 示例: '{"units": "miles"}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Point 特征
            - 类型: GeoJSON Feature with Point geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}, "properties": {"location": 距离起点位置, "distance": 距离值}}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> line = '{"type": "LineString", "coordinates": [[-77.031669, 38.878605], [-77.029609, 38.881946], [-77.020339, 38.884084], [-77.025661, 38.885821], [-77.021884, 38.889563], [-77.019824, 38.892368]]}'
        >>> point = '{"type": "Point", "coordinates": [-77.037076, 38.884017]}'
        >>> options = '{"units": "miles"}'
        >>> result = asyncio.run(nearest_point_on_line(line, point, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-77.03, 38.883]}, "properties": {"location": 0.5, "distance": 0.2}}'
    
    Notes:
        - 输入参数 line 和 point 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 返回线上距离给定点最近的位置及相关信息
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const line = JSON.parse('{line}');
        const point = JSON.parse('{point}');
        const options = JSON.parse('{options_param}');
        const result = turf.nearestPointOnLine(line, point, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@misc_mcp.tool
async def sector(center: str, radius: float, bearing1: float, bearing2: float, options: str = None) -> str:
    """
    创建扇形多边形区域。
    
    此功能以给定点为中心，创建指定半径和方位角范围的扇形多边形区域。
    
    Args:
        center: 中心点 GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-75, 40]}'
        
        radius: 扇形半径
            - 类型: float
            - 描述: 扇形的半径值
            - 示例: 5.0
        
        bearing1: 起始方位角
            - 类型: float
            - 描述: 扇形起始方位角（从北方向顺时针测量）
            - 示例: 25.0
        
        bearing2: 结束方位角
            - 类型: float
            - 描述: 扇形结束方位角（从北方向顺时针测量）
            - 示例: 45.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
                - steps: 扇形边界分段数 (默认: 64)
                - properties: 传递给扇形的属性对象
            - 示例: '{"units": "miles", "steps": 32}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON Polygon 特征
            - 类型: GeoJSON Feature with Polygon geometry
            - 格式: {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> center = '{"type": "Point", "coordinates": [-75, 40]}'
        >>> options = '{"units": "miles", "steps": 32}'
        >>> result = asyncio.run(sector(center, 5.0, 25.0, 45.0, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-75, 40], ...]]}}'
    
    Notes:
        - 输入参数 center 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 方位角是从北方向顺时针测量的角度
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const center = JSON.parse('{center}');
        const radius = parseFloat({radius});
        const bearing1 = parseFloat({bearing1});
        const bearing2 = parseFloat({bearing2});
        const options = JSON.parse('{options_param}');
        const result = turf.sector(center, radius, bearing1, bearing2, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@misc_mcp.tool
async def shortest_path(start_point: str, end_point: str, options: str = None) -> str:
    """
    计算两点之间的最短路径。
    
    此功能计算两个地理点之间的最短路径，考虑障碍物和地形因素，返回最优路径线段。
    
    Args:
        start_point: 起点 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-122, 48]}'
        
        end_point: 终点 GeoJSON Point 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Point 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Point", "coordinates": [-77, 39]}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - obstacles: 障碍物 GeoJSON 特征集合
                - resolution: 路径计算分辨率
                - properties: 传递给路径的属性对象
            - 示例: '{"resolution": 100}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON LineString 特征
            - 类型: GeoJSON Feature with LineString geometry
            - 格式: {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [...]}}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> start = '{"type": "Point", "coordinates": [-122, 48]}'
        >>> end = '{"type": "Point", "coordinates": [-77, 39]}'
        >>> options = '{"resolution": 100}'
        >>> result = asyncio.run(shortest_path(start, end, options))
        >>> print(result)
        '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-122, 48], ...]]}}'
    
    Notes:
        - 输入参数 start_point 和 end_point 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 计算两点之间的最短路径，考虑地理因素
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const startPoint = JSON.parse('{start_point}');
        const endPoint = JSON.parse('{end_point}');
        const options = JSON.parse('{options_param}');
        const result = turf.shortestPath(startPoint, endPoint, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@misc_mcp.tool
async def unkink_polygon(polygon: str) -> str:
    """
    消除多边形中的自相交部分。
    
    此功能检测并消除多边形中的自相交部分（扭结），返回无自相交的多边形集合。
    
    Args:
        polygon: 多边形 GeoJSON 特征或几何图形
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 必须符合 GeoJSON Polygon 规范
            - 坐标系: WGS84 (经度在前，纬度在后)
            - 示例: '{"type": "Polygon", "coordinates": [[[0, 0], [2, 0], [0, 2], [2, 2], [0, 0]]]}'
    
    Returns:
        str: JSON 字符串格式的多边形特征集合
            - 类型: GeoJSON FeatureCollection with Polygon features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}}, ...]}
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> polygon = '{"type": "Polygon", "coordinates": [[[0, 0], [2, 0], [0, 2], [2, 2], [0, 0]]]}'
        >>> result = asyncio.run(unkink_polygon(polygon))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0, 0], [1, 1], [0, 2], [0, 0]]]}}, {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[1, 1], [2, 0], [2, 2], [1, 1]]]}}]}'
    
    Notes:
        - 输入参数 polygon 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 消除多边形中的自相交部分，返回多个无自相交的多边形
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const polygon = JSON.parse('{polygon}');
        const result = turf.unkinkPolygon(polygon);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")
