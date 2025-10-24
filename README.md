![My Project Logo](./logo.png)

# Turf-MCP

基于 Turf.js 构建的地理空间分析 MCP 服务。

## 简介

Turf-MCP 是一个 Python 库，提供基于 Turf.js 的地理空间分析功能，通过 Model Context Protocol (MCP) 暴露为工具和资源。它支持空间几何图形的测量、空间关系判断、坐标转换与偏移等核心功能。

## 开始

### mcp server 配置
#### stdio 模式
##### Windows
```json
 {
  "mcpServers": {
   "turf-mcp-server": {
      "command": "cmd",
      "args": ["/c", "uvx", "turf-mcp"],
      "type": "stdio"
    } 
  }
}
```
##### macOS/Linux
```json
 {
  "mcpServers": {
   "turf-mcp-server": {
      "command": "uvx",
      "args": ["turf-mcp"],
      "type": "stdio"
    } 
  }
}
```



#### 远程模式
```shell
# sse
uvx turf-mcp -t sse -p 8080
# 访问路径：http://localhost:8080/sse

# http
uvx turf-mcp -t http -p 8080
# 访问路径：http://localhost:8080/mcp
```
对应的mcp server配置
```json
 {
  "mcpServers": {
     "turf-mcp-server": {
      "url": "http://127.0.0.1:8000/sse"
    } 
  }
}
```


## 功能特性

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
- `buffer` - 创建缓冲区
- `circle` - 根据中心点和半径创建圆形区域
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

## 环境依赖
- Python 3.10+
- node 14.x

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 参考文档
- [Turf.js](https://turfjs.org/)
- [FastMCP](https://gofastmcp.com/getting-started/welcome)

## 支持

- 文档: [GitHub Repository](https://github.com/es3154/turf-mcp)
- 问题: [GitHub Issues](https://github.com/es3154/turf-mcp/issues)

