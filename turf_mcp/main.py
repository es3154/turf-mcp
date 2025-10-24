import asyncio
import sys
import os
from typing import Literal

# 添加当前目录到 Python 路径，以便可以导入 turf_mcp 模块
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastmcp import FastMCP
from turf_mcp.server import (
    aggregation_mcp,
    booleans_mcp,
    classification_mcp,
    coordinate_mutation_mcp,
    data_mcp,
    feature_conversion_mcp,
    grid_mcp,
    helper_mcp,
    interpolation_mcp,
    joins_mcp,
    measurement_mcp,
    misc_mcp,
    random_mcp,
    transformation_mcp,
    unit_conversion_mcp
)


instructions = """
Turf.js MCP 服务器 - 地理空间分析和测量工具

这个 MCP 服务器基于 Turf.js 库提供全面的地理空间分析和计算功能。它支持各种几何操作、空间分析、数据转换和测量计算，专门用于处理 GeoJSON 格式的地理数据。

## 通用注意事项：

### 数据格式要求：
- 所有输入参数必须是有效的 JSON 字符串格式的 GeoJSON 对象
- 坐标系：WGS84（经度在前，纬度在后）
- 坐标顺序：[经度, 纬度]

### 单位系统：
- 距离单位：'miles', 'nauticalmiles', 'kilometers', 'meters', 'yards', 'feet', 'inches'
- 面积单位：平方米
- 方位角单位：度

### 依赖环境：
- 需要 Node.js 环境
- 依赖 @turf/turf 库
- 支持异步操作

### 错误处理：
- 当 JavaScript 执行失败、超时或输入数据格式错误时抛出异常
- 所有函数都返回 JSON 字符串格式的结果，便于后续处理和分析

## 功能模块分类：

### 1. 测量功能 (measurement)
**距离和长度计算：**
- `along` - 在 GeoJSON LineString 上计算指定距离处的点
- `distance` - 计算两个 GeoJSON 点特征之间的球面距离
- `length` - 计算 GeoJSON 线或多线几何图形的长度
- `rhumbDistance` - 计算两点之间的恒向线距离（等角航线距离）
- `pointToLineDistance` - 计算点到线的最短球面距离

**方位角计算：**
- `bearing` - 计算两点之间的地理方位角（从北方向顺时针测量）
- `rhumbBearing` - 计算两点之间的恒向线方位角

**中心点和位置计算：**
- `center` - 计算 GeoJSON 特征集合的绝对中心点
- `centerOfMass` - 计算 GeoJSON 对象的质心
- `centroid` - 计算 GeoJSON 对象的几何中心
- `midpoint` - 计算两个 GeoJSON 点特征之间的中点
- `pointOnFeature` - 在 GeoJSON 特征上找到最近的点

**边界和包络计算：**
- `bbox` - 计算 GeoJSON 对象的边界框
- `bboxPolygon` - 将边界框数组转换为 GeoJSON 多边形特征
- `envelope` - 计算 GeoJSON 对象的包络多边形（边界框多边形）
- `square` - 计算包含边界框的最小正方形边界框

**面积计算：**
- `area` - 计算 GeoJSON 多边形的大地测量面积

**路径和目标点计算：**
- `destination` - 从起点沿着指定方位角移动指定距离来计算目标点
- `rhumbDestination` - 沿恒向线计算目标点
- `greatCircle` - 计算两点之间的大圆路径（球面上最短路径）
- `polygonTangents` - 计算从给定点到多边形的两个切线点

### 2. 空间聚合和聚类 (aggregation)
- `collect` - 将点属性聚合到多边形中，用于统计和汇总分析
- `clustersDbscan` - 使用 DBSCAN 算法进行点聚类，识别密集区域
- `clustersKmeans` - 使用 K-means 算法进行点聚类，将点划分为指定数量的簇

### 3. 布尔运算 (booleans)
- `booleanClockwise` - 检查环是否为顺时针方向
- `booleanContains` - 检查第一个几何图形是否包含第二个几何图形
- `booleanCrosses` - 检查两个几何图形是否相交
- `booleanDisjoint` - 检查两个几何图形是否不相交
- `booleanEqual` - 检查两个几何图形是否相等
- `booleanOverlap` - 检查两个几何图形是否重叠
- `booleanParallel` - 检查两条线段是否平行
- `booleanPointInPolygon` - 检查点是否在多边形内部
- `booleanPointOnLine` - 检查点是否在线上
- `booleanWithin` - 检查第一个几何图形是否在第二个几何图形内部

### 4. 分类功能 (classification)
- `nearestPoint` - 查找距离目标点最近的点特征

### 5. 坐标转换和清理 (coordinate_mutation)
- `clean_coords` - 清理 GeoJSON 数据中的冗余坐标点
- `flip` - 交换坐标的经度和纬度位置
- `rewind` - 修正多边形的环方向，确保外环逆时针、内环顺时针
- `round_number` - 对数字进行四舍五入，控制小数位数
- `truncate` - 截断 GeoJSON 几何图形的坐标精度

### 6. 数据采样和处理 (data)
- `sample` - 从特征集合中随机采样指定数量的特征

### 7. 特征转换 (feature_conversion)
- `combine` - 将特征集合合并为复合几何图形
- `explode` - 将几何图形分解为单独的点特征
- `flatten` - 将复合几何图形展平为简单几何图形
- `line_to_polygon` - 将线转换为多边形
- `polygonize` - 将线几何图形转换为多边形
- `polygon_to_line` - 将多边形转换为线几何图形

### 8. 网格生成 (grid)
- `hexGrid` - 在边界框内生成六边形网格，用于空间分析和可视化
- `pointGrid` - 在边界框内生成点网格，用于空间采样和插值
- `squareGrid` - 在边界框内生成正方形网格，用于空间分析和区域划分
- `triangleGrid` - 在边界框内生成三角形网格，用于空间分析和表面建模

### 9. 几何对象创建辅助 (helper)
- `featureCollection` - 将多个地理特征组合成一个特征集合
- `feature` - 创建单个地理特征对象
- `geometryCollection` - 创建几何图形集合特征
- `lineString` - 创建线特征对象
- `multiLineString` - 创建多线特征对象
- `multiPoint` - 创建多点特征对象
- `multiPolygon` - 创建多多边形特征对象
- `point` - 创建点特征对象
- `polygon` - 创建多边形特征对象

### 10. 空间插值和表面分析 (interpolation)
- `interpolate` - 使用反距离权重法进行空间插值
- `isobands` - 从点网格生成等值带，用于创建连续值的区域表示
- `isolines` - 从点网格生成等值线，用于创建连续值的线状表示
- `planepoint` - 计算点在三角形平面上的z值
- `tin` - 从点集创建不规则三角网，用于表面建模和地形分析

### 11. 空间连接和属性关联 (joins)
- `pointsWithinPolygon` - 查找多边形内部的点
- `tag` - 为点特征添加多边形属性

### 12. 杂项地理操作 (misc)
- `kinks` - 查找几何图形中的自相交点
- `line_arc` - 创建圆弧线段
- `line_chunk` - 将线分割为指定长度的线段
- `line_intersect` - 计算两条线的交点
- `line_overlap` - 查找两条线的重叠部分
- `line_segment` - 将几何图形分解为线段
- `line_slice` - 在线段上截取指定起点和终点之间的部分
- `line_slice_along` - 沿线段长度截取指定距离范围的部分
- `line_split` - 用分割器将线段分割为多段
- `mask` - 使用掩膜多边形裁剪几何图形
- `nearest_point_on_line` - 找到线上距离给定点最近的位置
- `sector` - 创建扇形多边形区域
- `shortest_path` - 计算两点之间的最短路径
- `unkink_polygon` - 消除多边形中的自相交部分

### 13. 随机地理数据生成 (random)
- `randomPosition` - 生成随机的地理坐标位置
- `randomPoint` - 生成随机点特征集合
- `randomLineString` - 生成随机线特征集合
- `randomPolygon` - 生成随机多边形特征集合

### 14. 几何变换和操作 (transformation)
- `bboxClip` - 将 GeoJSON 特征裁剪到指定的边界框内
- `bezierSpline` - 将直线转换为平滑的贝塞尔曲线
- `circle` - 根据中心点和半径创建圆形区域
- `buffer` - 根据GeoJSON 特征创建指定半径的缓冲区多边形。
- `clone` - 创建 GeoJSON 对象的完整副本
- `concave` - 计算点集的凹包
- `convex` - 计算点集的凸包
- `difference` - 计算两个多边形的差异
- `dissolve` - 合并相邻的多边形
- `intersect` - 计算多边形的交集
- `lineOffset` - 计算线的偏移
- `simplify` - 简化 GeoJSON 几何
- `tesselate` - 将多边形分割为三角形
- `transformRotate` - 旋转 GeoJSON 对象
- `transformTranslate` - 平移 GeoJSON 对象
- `transformScale` - 缩放 GeoJSON 对象
- `union` - 合并两个多边形
- `voronoi` - 生成 Voronoi 多边形

### 15. 单位转换 (unit_conversion)
- `bearingToAzimuth` - 将方位角转换为方位角（0-360度范围）
- `convertArea` - 转换面积单位
- `convertLength` - 转换长度单位
- `degreesToRadians` - 将角度转换为弧度
- `lengthToRadians` - 将长度转换为弧度距离
- `lengthToDegrees` - 将长度转换为角度距离
- `radiansToLength` - 将弧度距离转换为长度
- `radiansToDegrees` - 将弧度转换为角度
- `toMercator` - 将地理坐标转换为墨卡托投影坐标
- `toWgs84` - 将墨卡托投影坐标转换为地理坐标

## 使用提示和最佳实践：

### 数据验证：
- 确保输入的 GeoJSON 数据格式正确，坐标顺序为 [经度, 纬度]
- 对于多边形几何，确保首尾坐标点相同形成闭合环
- 验证坐标值在有效范围内（经度：-180 到 180，纬度：-90 到 90）

### 性能优化：
- 对于大数据集，考虑使用简化操作减少几何复杂度
- 批量操作时使用异步处理提高效率
- 合理选择网格大小和插值参数以平衡精度和性能

### 错误处理：
- 所有函数都包含异常处理机制
- 建议在使用前验证输入数据的有效性
- 对于复杂操作，建议先进行小规模测试

### 应用场景示例：
- **地理分析**：使用测量功能计算距离、面积和方位角
- **空间统计**：使用聚合功能进行点数据聚类分析
- **数据可视化**：使用网格和插值功能创建热力图和等值线图
- **路径规划**：使用最短路径和路径分析功能
- **数据清理**：使用坐标转换和简化功能优化几何数据


请根据具体需求选择合适的模块前缀调用相应功能。
"""

main_mcp = FastMCP("turf-mcp-server", instructions=instructions)


async def install_turf():
    """安装turf.js"""
    try:
        # 在 Windows 上使用 npm.cmd，其他系统使用 npm
        npm_command = 'npm.cmd' if os.name == 'nt' else 'npm'
        
        # 使用 asyncio.create_subprocess_exec 异步执行命令
        process = await asyncio.create_subprocess_exec(
            npm_command, 'i', '@turf/turf',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # 等待结果
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=30)

        # 解码输出
        stdout = stdout.decode('utf-8', errors='ignore')
        stderr = stderr.decode('utf-8', errors='ignore')

        # 检查是否有错误
        if process.returncode != 0:
            raise Exception(f"turf.js安装失败: {stderr}")

        print(f"turf.js安装成功: {stdout}")

    except asyncio.TimeoutError:
        raise Exception("turf.js安装超时")
    except Exception as e:
        raise Exception(f"执行异常: {str(e)}")

async def init():

    await install_turf()

    # 导入所有 MCP 服务器
    await main_mcp.import_server(aggregation_mcp, prefix="aggregation")
    await main_mcp.import_server(booleans_mcp, prefix="booleans")
    await main_mcp.import_server(classification_mcp, prefix="classification")
    await main_mcp.import_server(coordinate_mutation_mcp, prefix="coordinate_mutation")
    await main_mcp.import_server(data_mcp, prefix="data")
    await main_mcp.import_server(feature_conversion_mcp, prefix="feature_conversion")
    await main_mcp.import_server(grid_mcp, prefix="grid")
    await main_mcp.import_server(helper_mcp, prefix="helper")
    await main_mcp.import_server(interpolation_mcp, prefix="interpolation")
    await main_mcp.import_server(joins_mcp, prefix="joins")
    await main_mcp.import_server(measurement_mcp, prefix="measurement")
    await main_mcp.import_server(misc_mcp, prefix="misc")
    await main_mcp.import_server(random_mcp, prefix="random")
    await main_mcp.import_server(transformation_mcp, prefix="transformation")
    await main_mcp.import_server(unit_conversion_mcp, prefix="unit_conversion")

Transport = Literal["stdio", "http", "sse", "streamable-http"]

def setup(transport: Transport="stdio", port=8000):
    """主函数"""
    asyncio.run(init())
    if transport == "stdio":
        main_mcp.run(transport=transport)
    else:
        main_mcp.run(transport=transport, host="0.0.0.0", port=port)

if __name__ == "__main__":
    setup(transport="sse")