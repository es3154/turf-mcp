# 数据采样和处理函数

from fastmcp import FastMCP

from turf_mcp.utils import call_js_script

data_mcp = FastMCP("data")

@data_mcp.tool
async def sample(feature_collection: str, num: int) -> str:
    """
    从特征集合中随机采样指定数量的特征。
    
    此功能从输入的特征集合中随机选择指定数量的特征，返回一个新的特征集合。
    
    Args:
        feature_collection: 输入特征集合
            - 类型: str (JSON 字符串格式的 GeoJSON FeatureCollection)
            - 格式: 任何有效的 GeoJSON FeatureCollection
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, ...]}'
        
        num: 采样数量
            - 类型: int
            - 描述: 要从输入集合中随机选择特征的数量
            - 示例: 5
    
    Returns:
        str: JSON 字符串格式的 GeoJSON FeatureCollection
            - 类型: GeoJSON FeatureCollection
            - 格式: {"type": "FeatureCollection", "features": [...]}
            - 示例: '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, ...]}'
    
    Raises:
        Exception: 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
    
    Example:
        >>> import asyncio
        >>> feature_collection = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, ...]}'
        >>> result = asyncio.run(sample(feature_collection, 5))
        >>> print(result)
        '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-75.343, 39.984]}}, ...]}'
    
    Notes:
        - 输入参数 feature_collection 必须是有效的 JSON 字符串
        - 采样数量不能超过输入特征集合中的特征总数
        - 如果采样数量为0，返回空的特征集合
        - 采样是随机进行的，每次调用可能得到不同的结果
        - 依赖于 Turf.js 库和 Node.js 环境
    """

    js_script = f"""
        const turf = require('@turf/turf');
        const featureCollection = JSON.parse('{feature_collection}');
        const num = parseInt({num});
        const result = turf.sample(featureCollection, num);
        console.log(JSON.stringify(result));
    """

    try:
        return await call_js_script(js_script)

    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")
