# 空间布尔运算函数

from fastmcp import FastMCP

from turf_mcp.utils import call_js_script

booleans_mcp = FastMCP("booleans")

@booleans_mcp.tool
async def booleanClockwise(ring: str) -> str:
    """
    检查环是否为顺时针方向。
    
    此功能检查给定的坐标环（多边形边界）是否为顺时针方向。
    
    Args:
        ring: 坐标环数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: [[x1, y1], [x2, y2], [x3, y3], ...]
            - 示例: '[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]'
    
    Returns:
        str: JSON 字符串格式的布尔结果
            - 类型: 包含 value 的对象
            - 格式: {"value": true 或 false}
            - 示例: '{"value": true}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> ring = '[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]'
        >>> result = asyncio.run(booleanClockwise(ring))
        >>> print(result)
        '{"value": true}'
    
    Notes:
        - 输入参数 ring 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 顺时针环在多边形中表示外部边界
        - 逆时针环在多边形中表示内部孔洞
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const ring = JSON.parse('{ring}');
        const result = turf.booleanClockwise(ring);
        console.log(JSON.stringify({{"value": result}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@booleans_mcp.tool
async def booleanContains(geojson1: str, geojson2: str) -> str:
    """
    检查第一个几何图形是否包含第二个几何图形。
    
    此功能检查第一个GeoJSON几何图形是否完全包含第二个几何图形。
    
    Args:
        geojson1: 第一个GeoJSON对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 示例: '{"type": "Polygon", "coordinates": [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]]}'
        
        geojson2: 第二个GeoJSON对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 示例: '{"type": "Point", "coordinates": [1, 1]}'
    
    Returns:
        str: JSON 字符串格式的布尔结果
            - 类型: 包含 value 的对象
            - 格式: {"value": true 或 false}
            - 示例: '{"value": true}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson1 = '{"type": "Polygon", "coordinates": [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]]}'
        >>> geojson2 = '{"type": "Point", "coordinates": [1, 1]}'
        >>> result = asyncio.run(booleanContains(geojson1, geojson2))
        >>> print(result)
        '{"value": true}'
    
    Notes:
        - 输入参数 geojson1 和 geojson2 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 包含关系要求第二个几何图形完全在第一个几何图形内部
        - 边界接触不被视为包含
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson1 = JSON.parse('{geojson1}');
        const geojson2 = JSON.parse('{geojson2}');
        const result = turf.booleanContains(geojson1, geojson2);
        console.log(JSON.stringify({{"value": result}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@booleans_mcp.tool
async def booleanCrosses(geojson1: str, geojson2: str) -> str:
    """
    检查两个几何图形是否相交。
    
    此功能检查两个GeoJSON几何图形是否相交（交叉但不相交于边界点）。
    
    Args:
        geojson1: 第一个GeoJSON对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 示例: '{"type": "LineString", "coordinates": [[0, 0], [2, 2]]}'
        
        geojson2: 第二个GeoJSON对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 示例: '{"type": "LineString", "coordinates": [[0, 2], [2, 0]]}'
    
    Returns:
        str: JSON 字符串格式的布尔结果
            - 类型: 包含 value 的对象
            - 格式: {"value": true 或 false}
            - 示例: '{"value": true}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson1 = '{"type": "LineString", "coordinates": [[0, 0], [2, 2]]}'
        >>> geojson2 = '{"type": "LineString", "coordinates": [[0, 2], [2, 0]]}'
        >>> result = asyncio.run(booleanCrosses(geojson1, geojson2))
        >>> print(result)
        '{"value": true}'
    
    Notes:
        - 输入参数 geojson1 和 geojson2 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 交叉关系要求几何图形在内部点相交
        - 边界接触不被视为交叉
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson1 = JSON.parse('{geojson1}');
        const geojson2 = JSON.parse('{geojson2}');
        const result = turf.booleanCrosses(geojson1, geojson2);
        console.log(JSON.stringify({{"value": result}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@booleans_mcp.tool
async def booleanDisjoint(geojson1: str, geojson2: str) -> str:
    """
    检查两个几何图形是否不相交。
    
    此功能检查两个GeoJSON几何图形是否完全不相交（没有共同点）。
    
    Args:
        geojson1: 第一个GeoJSON对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 示例: '{"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]}'
        
        geojson2: 第二个GeoJSON对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 示例: '{"type": "Polygon", "coordinates": [[[2, 2], [3, 2], [3, 3], [2, 3], [2, 2]]]}'
    
    Returns:
        str: JSON 字符串格式的布尔结果
            - 类型: 包含 value 的对象
            - 格式: {"value": true 或 false}
            - 示例: '{"value": true}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson1 = '{"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]}'
        >>> geojson2 = '{"type": "Polygon", "coordinates": [[[2, 2], [3, 2], [3, 3], [2, 3], [2, 2]]]}'
        >>> result = asyncio.run(booleanDisjoint(geojson1, geojson2))
        >>> print(result)
        '{"value": true}'
    
    Notes:
        - 输入参数 geojson1 和 geojson2 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 不相交关系要求几何图形没有任何共同点
        - 边界接触也被视为相交
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson1 = JSON.parse('{geojson1}');
        const geojson2 = JSON.parse('{geojson2}');
        const result = turf.booleanDisjoint(geojson1, geojson2);
        console.log(JSON.stringify({{"value": result}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@booleans_mcp.tool
async def booleanEqual(geojson1: str, geojson2: str) -> str:
    """
    检查两个几何图形是否相等。
    
    此功能检查两个GeoJSON几何图形是否在几何上完全相等。
    
    Args:
        geojson1: 第一个GeoJSON对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 示例: '{"type": "Point", "coordinates": [1, 1]}'
        
        geojson2: 第二个GeoJSON对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 示例: '{"type": "Point", "coordinates": [1, 1]}'
    
    Returns:
        str: JSON 字符串格式的布尔结果
            - 类型: 包含 value 的对象
            - 格式: {"value": true 或 false}
            - 示例: '{"value": true}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson1 = '{"type": "Point", "coordinates": [1, 1]}'
        >>> geojson2 = '{"type": "Point", "coordinates": [1, 1]}'
        >>> result = asyncio.run(booleanEqual(geojson1, geojson2))
        >>> print(result)
        '{"value": true}'
    
    Notes:
        - 输入参数 geojson1 和 geojson2 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 相等关系要求几何图形具有相同的坐标和结构
        - 属性不同不影响几何相等性判断
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson1 = JSON.parse('{geojson1}');
        const geojson2 = JSON.parse('{geojson2}');
        const result = turf.booleanEqual(geojson1, geojson2);
        console.log(JSON.stringify({{"value": result}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@booleans_mcp.tool
async def booleanOverlap(geojson1: str, geojson2: str) -> str:
    """
    检查两个几何图形是否重叠。
    
    此功能检查两个GeoJSON几何图形是否在空间上重叠（有共同区域但不完全包含）。
    
    Args:
        geojson1: 第一个GeoJSON对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 示例: '{"type": "Polygon", "coordinates": [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]]}'
        
        geojson2: 第二个GeoJSON对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 示例: '{"type": "Polygon", "coordinates": [[[1, 1], [3, 1], [3, 3], [1, 3], [1, 1]]]}'
    
    Returns:
        str: JSON 字符串格式的布尔结果
            - 类型: 包含 value 的对象
            - 格式: {"value": true 或 false}
            - 示例: '{"value": true}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson1 = '{"type": "Polygon", "coordinates": [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]]}'
        >>> geojson2 = '{"type": "Polygon", "coordinates": [[[1, 1], [3, 1], [3, 3], [1, 3], [1, 1]]]}'
        >>> result = asyncio.run(booleanOverlap(geojson1, geojson2))
        >>> print(result)
        '{"value": true}'
    
    Notes:
        - 输入参数 geojson1 和 geojson2 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 重叠关系要求几何图形有共同区域但互不包含
        - 边界接触不被视为重叠
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson1 = JSON.parse('{geojson1}');
        const geojson2 = JSON.parse('{geojson2}');
        const result = turf.booleanOverlap(geojson1, geojson2);
        console.log(JSON.stringify({{"value": result}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@booleans_mcp.tool
async def booleanParallel(line1: str, line2: str) -> str:
    """
    检查两条线段是否平行。
    
    此功能检查两条线段是否在几何上平行。
    
    Args:
        line1: 第一条线段
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: Feature with LineString geometry
            - 示例: '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 1]]}}'
        
        line2: 第二条线段
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: Feature with LineString geometry
            - 示例: '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[0, 1], [1, 2]]}}'
    
    Returns:
        str: JSON 字符串格式的布尔结果
            - 类型: 包含 value 的对象
            - 格式: {"value": true 或 false}
            - 示例: '{"value": true}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> line1 = '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 1]]}}'
        >>> line2 = '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[0, 1], [1, 2]]}}'
        >>> result = asyncio.run(booleanParallel(line1, line2))
        >>> print(result)
        '{"value": true}'
    
    Notes:
        - 输入参数 line1 和 line2 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 平行关系基于线段的方向向量
        - 允许一定的数值容差
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const line1 = JSON.parse('{line1}');
        const line2 = JSON.parse('{line2}');
        const result = turf.booleanParallel(line1, line2);
        console.log(JSON.stringify({{"value": result}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@booleans_mcp.tool
async def booleanPointInPolygon(point: str, polygon: str, options: str = None) -> str:
    """
    检查点是否在多边形内部。
    
    此功能检查点是否位于多边形或多边形集合的内部。
    
    Args:
        point: 点特征
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: Feature with Point geometry
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [1, 1]}}'
        
        polygon: 多边形特征
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: Feature with Polygon or MultiPolygon geometry
            - 示例: '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]]}}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - ignoreBoundary: 是否忽略边界 (默认: false)
            - 示例: '{"ignoreBoundary": true}'
    
    Returns:
        str: JSON 字符串格式的布尔结果
            - 类型: 包含 value 的对象
            - 格式: {"value": true 或 false}
            - 示例: '{"value": true}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> point = '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [1, 1]}}'
        >>> polygon = '{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]]}}'
        >>> result = asyncio.run(booleanPointInPolygon(point, polygon))
        >>> print(result)
        '{"value": true}'
    
    Notes:
        - 输入参数 point 和 polygon 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 使用射线法算法判断点是否在多边形内部
        - 边界上的点默认被视为内部
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const point = JSON.parse('{point}');
        const polygon = JSON.parse('{polygon}');
        const options = JSON.parse('{options_param}');
        const result = turf.booleanPointInPolygon(point, polygon, options);
        console.log(JSON.stringify({{"value": result}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@booleans_mcp.tool
async def booleanPointOnLine(point: str, line: str, options: str = None) -> str:
    """
    检查点是否在线上。
    
    此功能检查点是否位于线段或多线的路径上。
    
    Args:
        point: 点特征
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: Feature with Point geometry
            - 示例: '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [1, 1]}}'
        
        line: 线特征
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: Feature with LineString or MultiLineString geometry
            - 示例: '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[0, 0], [2, 2]]}}'
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - ignoreEndVertices: 是否忽略端点 (默认: false)
            - 示例: '{"ignoreEndVertices": true}'
    
    Returns:
        str: JSON 字符串格式的布尔结果
            - 类型: 包含 value 的对象
            - 格式: {"value": true 或 false}
            - 示例: '{"value": true}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> point = '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [1, 1]}}'
        >>> line = '{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[0, 0], [2, 2]]}}'
        >>> result = asyncio.run(booleanPointOnLine(point, line))
        >>> print(result)
        '{"value": true}'
    
    Notes:
        - 输入参数 point 和 line 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 使用点到线段距离算法判断点是否在线上
        - 允许一定的数值容差
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const point = JSON.parse('{point}');
        const line = JSON.parse('{line}');
        const options = JSON.parse('{options_param}');
        const result = turf.booleanPointOnLine(point, line, options);
        console.log(JSON.stringify({{"value": result}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@booleans_mcp.tool
async def booleanWithin(geojson1: str, geojson2: str) -> str:
    """
    检查第一个几何图形是否在第二个几何图形内部。
    
    此功能检查第一个GeoJSON几何图形是否完全位于第二个几何图形内部。
    
    Args:
        geojson1: 第一个GeoJSON对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 示例: '{"type": "Point", "coordinates": [1, 1]}'
        
        geojson2: 第二个GeoJSON对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 示例: '{"type": "Polygon", "coordinates": [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]]}'
    
    Returns:
        str: JSON 字符串格式的布尔结果
            - 类型: 包含 value 的对象
            - 格式: {"value": true 或 false}
            - 示例: '{"value": true}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson1 = '{"type": "Point", "coordinates": [1, 1]}'
        >>> geojson2 = '{"type": "Polygon", "coordinates": [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]]}'
        >>> result = asyncio.run(booleanWithin(geojson1, geojson2))
        >>> print(result)
        '{"value": true}'
    
    Notes:
        - 输入参数 geojson1 和 geojson2 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 内部关系要求第一个几何图形完全在第二个几何图形内部
        - 边界接触不被视为内部
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson1 = JSON.parse('{geojson1}');
        const geojson2 = JSON.parse('{geojson2}');
        const result = turf.booleanWithin(geojson1, geojson2);
        console.log(JSON.stringify({{"value": result}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")
