# 数据转换脚本

这个目录包含用于将军事数据从Excel格式转换为JSON格式的脚本，以便在Web前端应用程序中使用。

## 脚本说明

### 0. convert_all.py

一键运行所有数据转换脚本的批处理脚本。

#### 功能：

- 按顺序运行data_converter.py和country_metadata.py
- 提供执行状态和统计信息
- 记录运行时间和成功/失败情况

#### 使用方法：

```bash
python convert_all.py
```

### 1. data_converter.py

将rbdata目录中的Excel军事数据转换为JSON格式。

#### 功能：

- 读取rbdata目录中的Excel文件（african.xlsx, american.xlsx, aisan.xlsx, europen.xlsx, easternasian.xlsx, current_data.xlsx）
- 处理数据，包括设置列名、处理缺失值和数据类型转换
- 生成以下JSON文件：
  - 每个大洲的数据文件（african.json, american.json等）
  - 合并后的所有数据（all_military_data.json）
  - 按年份分组的数据（year_1960.json到year_2022.json）
  - 年份数据摘要（years_summary.json）

#### 使用方法：

```bash
python data_converter.py
```

### 2. country_metadata.py

生成包含国家ISO代码和地理坐标的元数据JSON文件，用于地图可视化。

#### 功能：

- 从转换后的JSON数据文件中提取国家列表
- 为国家生成ISO代码和地理坐标信息
- 生成country_metadata.json文件

#### 使用方法：

```bash
python country_metadata.py
```

## 数据结构

### 1. all_military_data.json

包含所有国家所有年份的军费开支数据。

```json
[
  {
    "Country": "国家名称",
    "1960": 军费开支数值,
    "1961": 军费开支数值,
    ...
    "2022": 军费开支数值,
    "Continent": "所属大洲"
  },
  ...
]
```

### 2. year_YYYY.json

包含特定年份所有国家的军费开支数据。

```json
[
  {
    "Country": "国家名称",
    "Continent": "所属大洲",
    "Expenditure": 军费开支数值
  },
  ...
]
```

### 3. years_summary.json

包含所有年份的摘要数据。

```json
{
  "1960": {
    "total_countries": 有数据的国家数量,
    "file": "year_1960.json",
    "total_expenditure": 全球总军费开支
  },
  ...
}
```

### 4. country_metadata.json

包含国家的元数据信息。

```json
{
  "国家名称": {
    "iso_code": "三字母ISO代码",
    "coordinates": {
      "lat": 纬度,
      "lon": 经度
    }
  },
  ...
}
```

## 注意事项

1. 运行脚本前请确保已安装所需的Python包：
   ```bash
   pip install pandas numpy openpyxl
   ```

2. 脚本会自动创建输出目录（web/public/data），如果该目录不存在。

3. 如果要添加更多国家的ISO代码和坐标信息，请在country_metadata.py中的相应函数中添加。

4. 建议使用convert_all.py脚本一次性运行所有转换，这样可以确保数据格式和依赖关系正确。 