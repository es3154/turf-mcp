# 单位转换函数

from fastmcp import FastMCP

from turf_mcp.utils import call_js_script

unit_conversion_mcp = FastMCP("unit_conversion")

@unit_conversion_mcp.tool
async def bearingToAzimuth(bearing: float) -> str:
    """
    将方位角转换为方位角（0-360度范围）。
    
    此功能将任意角度的方位角转换为0到360度范围内的标准方位角。
    
    Args:
        bearing: 方位角
            - 类型: float
            - 描述: 输入方位角（可以是任意角度）
            - 示例: -45.0
    
    Returns:
        str: JSON 字符串格式的方位角结果
            - 类型: 包含 value 和 units 的对象
            - 格式: {"value": 方位角数值, "units": "degrees"}
            - 示例: '{"value": 315.0, "units": "degrees"}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> result = asyncio.run(bearingToAzimuth(-45.0))
        >>> print(result)
        '{"value": 315.0, "units": "degrees"}'
    
    Notes:
        - 输入方位角可以是任意角度值
        - 输出方位角始终在0到360度范围内
        - 常用于标准化方位角表示
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const bearing = parseFloat({bearing});
        const result = turf.bearingToAzimuth(bearing);
        console.log(JSON.stringify({{"value": result, "units": "degrees"}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@unit_conversion_mcp.tool
async def convertArea(area: float, original_unit: str, final_unit: str) -> str:
    """
    转换面积单位。
    
    此功能将面积值从一种单位转换为另一种单位。
    
    Args:
        area: 面积值
            - 类型: float
            - 描述: 要转换的面积数值
            - 示例: 1000.0
        
        original_unit: 原始单位
            - 类型: str
            - 描述: 输入面积的单位
            - 有效值: 'meters', 'metres', 'centimeters', 'centimetres', 'millimeters', 'millimetres', 'acres', 'miles', 'nauticalmiles', 'inches', 'yards', 'feet', 'kilometers', 'hectares'
            - 示例: 'meters'
        
        final_unit: 目标单位
            - 类型: str
            - 描述: 输出面积的单位
            - 有效值: 'meters', 'metres', 'centimeters', 'centimetres', 'millimeters', 'millimetres', 'acres', 'miles', 'nauticalmiles', 'inches', 'yards', 'feet', 'kilometers', 'hectares'
            - 示例: 'acres'
    
    Returns:
        str: JSON 字符串格式的面积结果
            - 类型: 包含 value 和 units 的对象
            - 格式: {"value": 面积数值, "units": "目标单位"}
            - 示例: '{"value": 0.2471, "units": "acres"}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> result = asyncio.run(convertArea(1000.0, 'meters', 'acres'))
        >>> print(result)
        '{"value": 0.2471, "units": "acres"}'
    
    Notes:
        - 支持多种面积单位之间的转换
        - 输入和输出单位必须是有效的单位标识符
        - 转换基于标准单位换算系数
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const area = parseFloat({area});
        const originalUnit = '{original_unit}';
        const finalUnit = '{final_unit}';
        const result = turf.convertArea(area, originalUnit, finalUnit);
        console.log(JSON.stringify({{"value": result, "units": finalUnit}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@unit_conversion_mcp.tool
async def convertLength(length: float, original_unit: str, final_unit: str) -> str:
    """
    转换长度单位。
    
    此功能将长度值从一种单位转换为另一种单位。
    
    Args:
        length: 长度值
            - 类型: float
            - 描述: 要转换的长度数值
            - 示例: 1000.0
        
        original_unit: 原始单位
            - 类型: str
            - 描述: 输入长度的单位
            - 有效值: 'meters', 'metres', 'millimeters', 'millimetres', 'centimeters', 'centimetres', 'kilometers', 'kilometres', 'miles', 'nauticalmiles', 'inches', 'yards', 'feet'
            - 示例: 'meters'
        
        final_unit: 目标单位
            - 类型: str
            - 描述: 输出长度的单位
            - 有效值: 'meters', 'metres', 'millimeters', 'millimetres', 'centimeters', 'centimetres', 'kilometers', 'kilometres', 'miles', 'nauticalmiles', 'inches', 'yards', 'feet'
            - 示例: 'kilometers'
    
    Returns:
        str: JSON 字符串格式的长度结果
            - 类型: 包含 value 和 units 的对象
            - 格式: {"value": 长度数值, "units": "目标单位"}
            - 示例: '{"value": 1.0, "units": "kilometers"}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> result = asyncio.run(convertLength(1000.0, 'meters', 'kilometers'))
        >>> print(result)
        '{"value": 1.0, "units": "kilometers"}'
    
    Notes:
        - 支持多种长度单位之间的转换
        - 输入和输出单位必须是有效的单位标识符
        - 转换基于标准单位换算系数
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const length = parseFloat({length});
        const originalUnit = '{original_unit}';
        const finalUnit = '{final_unit}';
        const result = turf.convertLength(length, originalUnit, finalUnit);
        console.log(JSON.stringify({{"value": result, "units": finalUnit}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@unit_conversion_mcp.tool
async def degreesToRadians(degrees: float) -> str:
    """
    将角度转换为弧度。
    
    此功能将角度值转换为弧度值。
    
    Args:
        degrees: 角度值
            - 类型: float
            - 描述: 要转换的角度数值
            - 示例: 180.0
    
    Returns:
        str: JSON 字符串格式的弧度结果
            - 类型: 包含 value 和 units 的对象
            - 格式: {"value": 弧度数值, "units": "radians"}
            - 示例: '{"value": 3.14159, "units": "radians"}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> result = asyncio.run(degreesToRadians(180.0))
        >>> print(result)
        '{"value": 3.14159, "units": "radians"}'
    
    Notes:
        - 转换公式: 弧度 = 角度 × π / 180
        - 常用于数学计算和三角函数
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const degrees = parseFloat({degrees});
        const result = turf.degreesToRadians(degrees);
        console.log(JSON.stringify({{"value": result, "units": "radians"}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@unit_conversion_mcp.tool
async def lengthToRadians(distance: float, units: str = 'kilometers') -> str:
    """
    将长度转换为弧度距离。
    
    此功能将地面距离转换为对应的弧度距离（基于地球半径）。
    
    Args:
        distance: 距离值
            - 类型: float
            - 描述: 要转换的距离数值
            - 示例: 100.0
        
        units: 距离单位
            - 类型: str
            - 描述: 输入距离的单位
            - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
            - 默认: 'kilometers'
            - 示例: 'kilometers'
    
    Returns:
        str: JSON 字符串格式的弧度结果
            - 类型: 包含 value 和 units 的对象
            - 格式: {"value": 弧度数值, "units": "radians"}
            - 示例: '{"value": 0.0157, "units": "radians"}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> result = asyncio.run(lengthToRadians(100.0, 'kilometers'))
        >>> print(result)
        '{"value": 0.0157, "units": "radians"}'
    
    Notes:
        - 基于地球半径计算弧度距离
        - 常用于球面几何计算
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const distance = parseFloat({distance});
        const units = '{units}';
        const result = turf.lengthToRadians(distance, units);
        console.log(JSON.stringify({{"value": result, "units": "radians"}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@unit_conversion_mcp.tool
async def lengthToDegrees(distance: float, units: str = 'kilometers') -> str:
    """
    将长度转换为角度距离。
    
    此功能将地面距离转换为对应的角度距离（基于地球半径）。
    
    Args:
        distance: 距离值
            - 类型: float
            - 描述: 要转换的距离数值
            - 示例: 100.0
        
        units: 距离单位
            - 类型: str
            - 描述: 输入距离的单位
            - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
            - 默认: 'kilometers'
            - 示例: 'kilometers'
    
    Returns:
        str: JSON 字符串格式的角度结果
            - 类型: 包含 value 和 units 的对象
            - 格式: {"value": 角度数值, "units": "degrees"}
            - 示例: '{"value": 0.9, "units": "degrees"}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> result = asyncio.run(lengthToDegrees(100.0, 'kilometers'))
        >>> print(result)
        '{"value": 0.9, "units": "degrees"}'
    
    Notes:
        - 基于地球半径计算角度距离
        - 转换公式: 角度 = 距离 / (地球半径 × π / 180)
        - 常用于地理坐标计算
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const distance = parseFloat({distance});
        const units = '{units}';
        const result = turf.lengthToDegrees(distance, units);
        console.log(JSON.stringify({{"value": result, "units": "degrees"}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@unit_conversion_mcp.tool
async def radiansToLength(radians: float, units: str = 'kilometers') -> str:
    """
    将弧度距离转换为长度。
    
    此功能将弧度距离转换为对应的地面距离（基于地球半径）。
    
    Args:
        radians: 弧度值
            - 类型: float
            - 描述: 要转换的弧度数值
            - 示例: 0.1
        
        units: 距离单位
            - 类型: str
            - 描述: 输出距离的单位
            - 有效值: 'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
            - 默认: 'kilometers'
            - 示例: 'kilometers'
    
    Returns:
        str: JSON 字符串格式的长度结果
            - 类型: 包含 value 和 units 的对象
            - 格式: {"value": 长度数值, "units": "目标单位"}
            - 示例: '{"value": 637.1, "units": "kilometers"}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> result = asyncio.run(radiansToLength(0.1, 'kilometers'))
        >>> print(result)
        '{"value": 637.1, "units": "kilometers"}'
    
    Notes:
        - 基于地球半径计算地面距离
        - 转换公式: 距离 = 弧度 × 地球半径
        - 常用于球面几何计算
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const radians = parseFloat({radians});
        const units = '{units}';
        const result = turf.radiansToLength(radians, units);
        console.log(JSON.stringify({{"value": result, "units": units}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@unit_conversion_mcp.tool
async def radiansToDegrees(radians: float) -> str:
    """
    将弧度转换为角度。
    
    此功能将弧度值转换为角度值。
    
    Args:
        radians: 弧度值
            - 类型: float
            - 描述: 要转换的弧度数值
            - 示例: 3.14159
    
    Returns:
        str: JSON 字符串格式的角度结果
            - 类型: 包含 value 和 units 的对象
            - 格式: {"value": 角度数值, "units": "degrees"}
            - 示例: '{"value": 180.0, "units": "degrees"}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> result = asyncio.run(radiansToDegrees(3.14159))
        >>> print(result)
        '{"value": 180.0, "units": "degrees"}'
    
    Notes:
        - 转换公式: 角度 = 弧度 × 180 / π
        - 常用于数学计算和三角函数
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const radians = parseFloat({radians});
        const result = turf.radiansToDegrees(radians);
        console.log(JSON.stringify({{"value": result, "units": "degrees"}}));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@unit_conversion_mcp.tool
async def toMercator(geojson: str) -> str:
    """
    将地理坐标转换为墨卡托投影坐标。
    
    此功能将WGS84地理坐标转换为Web墨卡托投影坐标（EPSG:3857）。
    
    Args:
        geojson: GeoJSON对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象
            - 示例: '{"type": "Point", "coordinates": [-75.343, 39.984]}'
    
    Returns:
        str: JSON 字符串格式的墨卡托投影 GeoJSON
            - 类型: 相同的 GeoJSON 类型，但坐标为墨卡托投影
            - 格式: {"type": "Point", "coordinates": [x, y]}
            - 示例: '{"type": "Point", "coordinates": [-8385846.33, 4852834.51]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson = '{"type": "Point", "coordinates": [-75.343, 39.984]}'
        >>> result = asyncio.run(toMercator(geojson))
        >>> print(result)
        '{"type": "Point", "coordinates": [-8385846.33, 4852834.51]}'
    
    Notes:
        - 输入坐标必须是WGS84地理坐标（经度/纬度）
        - 输出坐标为Web墨卡托投影坐标（EPSG:3857）
        - 常用于Web地图显示（如Google Maps、OpenStreetMap）
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const result = turf.toMercator(geojson);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")


@unit_conversion_mcp.tool
async def toWgs84(geojson: str) -> str:
    """
    将墨卡托投影坐标转换为地理坐标。
    
    此功能将Web墨卡托投影坐标（EPSG:3857）转换为WGS84地理坐标。
    
    Args:
        geojson: GeoJSON对象
            - 类型: str (JSON 字符串格式的 GeoJSON)
            - 格式: 任何有效的 GeoJSON 对象（墨卡托投影坐标）
            - 示例: '{"type": "Point", "coordinates": [-8385846.33, 4852834.51]}'
    
    Returns:
        str: JSON 字符串格式的WGS84地理坐标 GeoJSON
            - 类型: 相同的 GeoJSON 类型，但坐标为WGS84地理坐标
            - 格式: {"type": "Point", "coordinates": [lng, lat]}
            - 示例: '{"type": "Point", "coordinates": [-75.343, 39.984]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> geojson = '{"type": "Point", "coordinates": [-8385846.33, 4852834.51]}'
        >>> result = asyncio.run(toWgs84(geojson))
        >>> print(result)
        '{"type": "Point", "coordinates": [-75.343, 39.984]}'
    
    Notes:
        - 输入坐标必须是Web墨卡托投影坐标（EPSG:3857）
        - 输出坐标为WGS84地理坐标（经度/纬度）
        - 常用于坐标系统转换
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const geojson = JSON.parse('{geojson}');
        const result = turf.toWgs84(geojson);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")
