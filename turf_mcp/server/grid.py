# 网格生成函数

from fastmcp import FastMCP

from turf_mcp.utils import call_js_script

grid_mcp = FastMCP("grid")

@grid_mcp.tool
async def hexGrid(bbox: str, cell_size: float, options: str = None) -> str:
    """
    在边界框内生成六边形网格。
    
    此功能在指定的边界框内创建六边形网格，用于空间分析和可视化。
    
    Args:
        bbox: 边界框数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: [minX, minY, maxX, maxY]
            - 示例: '[-180, -90, 180, 90]'
        
        cell_size: 网格单元大小
            - 类型: float
            - 描述: 六边形外接圆的半径
            - 示例: 50.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
                - properties: 传递给所有六边形的属性对象
                - mask: 用于裁剪网格的多边形特征
            - 示例: '{"units": "miles", "properties": {"type": "hexagon"}}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Polygon features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}, "properties": {...}}, ...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}, "properties": {"type": "hexagon"}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> bbox = '[-180, -90, 180, 90]'
        >>> result = asyncio.run(hexGrid(bbox, 50.0, '{"units": "miles"}'))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}, "properties": {...}}, ...]}'
    
    Notes:
        - 输入参数 bbox 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 六边形网格提供均匀的空间覆盖，常用于地理分析
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const bbox = JSON.parse('{bbox}');
        const cellSize = parseFloat({cell_size});
        const options = JSON.parse('{options_param}');
        const result = turf.hexGrid(bbox, cellSize, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@grid_mcp.tool
async def pointGrid(bbox: str, cell_size: float, options: str = None) -> str:
    """
    在边界框内生成点网格。
    
    此功能在指定的边界框内创建规则分布的点网格，用于空间采样和插值。
    
    Args:
        bbox: 边界框数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: [minX, minY, maxX, maxY]
            - 示例: '[-180, -90, 180, 90]'
        
        cell_size: 网格单元大小
            - 类型: float
            - 描述: 点之间的间距
            - 示例: 50.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
                - properties: 传递给所有点的属性对象
                - mask: 用于裁剪网格的多边形特征
            - 示例: '{"units": "miles", "properties": {"type": "grid_point"}}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Point features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [lng, lat]}, "properties": {...}}, ...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}, "properties": {"type": "grid_point"}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> bbox = '[-180, -90, 180, 90]'
        >>> result = asyncio.run(pointGrid(bbox, 50.0, '{"units": "miles"}'))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}, "properties": {"type": "grid_point"}}, ...]}'
    
    Notes:
        - 输入参数 bbox 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 点网格提供规则的空间采样点，常用于插值和统计
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const bbox = JSON.parse('{bbox}');
        const cellSize = parseFloat({cell_size});
        const options = JSON.parse('{options_param}');
        const result = turf.pointGrid(bbox, cellSize, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@grid_mcp.tool
async def squareGrid(bbox: str, cell_size: float, options: str = None) -> str:
    """
    在边界框内生成正方形网格。
    
    此功能在指定的边界框内创建正方形网格，用于空间分析和区域划分。
    
    Args:
        bbox: 边界框数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: [minX, minY, maxX, maxY]
            - 示例: '[-180, -90, 180, 90]'
        
        cell_size: 网格单元大小
            - 类型: float
            - 描述: 正方形的边长
            - 示例: 50.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
                - properties: 传递给所有正方形的属性对象
                - mask: 用于裁剪网格的多边形特征
            - 示例: '{"units": "miles", "properties": {"type": "square"}}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Polygon features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}, "properties": {...}}, ...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}, "properties": {"type": "square"}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> bbox = '[-180, -90, 180, 90]'
        >>> result = asyncio.run(squareGrid(bbox, 50.0, '{"units": "miles"}'))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}, "properties": {"type": "square"}}, ...]}'
    
    Notes:
        - 输入参数 bbox 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 正方形网格提供规则的矩形区域，常用于统计和聚合
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const bbox = JSON.parse('{bbox}');
        const cellSize = parseFloat({cell_size});
        const options = JSON.parse('{options_param}');
        const result = turf.squareGrid(bbox, cellSize, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@grid_mcp.tool
async def triangleGrid(bbox: str, cell_size: float, options: str = None) -> str:
    """
    在边界框内生成三角形网格。
    
    此功能在指定的边界框内创建三角形网格，用于空间分析和表面建模。
    
    Args:
        bbox: 边界框数组
            - 类型: str (JSON 字符串格式的数组)
            - 格式: [minX, minY, maxX, maxY]
            - 示例: '[-180, -90, 180, 90]'
        
        cell_size: 网格单元大小
            - 类型: float
            - 描述: 三角形每条边的长度
            - 示例: 50.0
        
        options: 可选参数配置
            - 类型: str (JSON 字符串) 或 None
            - 可选字段:
                - units: 距离单位 (默认: 'kilometers')
                    - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
                - properties: 传递给所有三角形的属性对象
                - mask: 用于裁剪网格的多边形特征
            - 示例: '{"units": "miles", "properties": {"type": "triangle"}}'
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection with Polygon features
            - 格式: {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}, "properties": {...}}, ...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}, "properties": {"type": "triangle"}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> bbox = '[-180, -90, 180, 90]'
        >>> result = asyncio.run(triangleGrid(bbox, 50.0, '{"units": "miles"}'))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [...]}, "properties": {"type": "triangle"}}, ...]}'
    
    Notes:
        - 输入参数 bbox 和 options 必须是有效的 JSON 字符串
        - 坐标顺序为 [经度, 纬度] (WGS84 坐标系)
        - 三角形网格提供灵活的空间划分，常用于表面建模
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    options_param = options if options else '{}'
    
    js_script = f"""
        const turf = require('@turf/turf');
        const bbox = JSON.parse('{bbox}');
        const cellSize = parseFloat({cell_size});
        const options = JSON.parse('{options_param}');
        const result = turf.triangleGrid(bbox, cellSize, options);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")
