package com.military.visualization.data.model

/**
 * 军事数据模型
 * 
 * @property country 国家名称
 * @property year 年份
 * @property expenditure 军费开支（百万美元）
 * @property gdpPercentage 军费占GDP百分比
 * @property perCapita 人均军费开支（美元）
 */
data class MilitaryData(
    val country: String,
    val year: Int,
    val expenditure: Double,
    val gdpPercentage: Double? = null,
    val perCapita: Double? = null
)

/**
 * 国家信息
 * 
 * @property name 国家名称
 * @property continent 所属大洲
 * @property isoCode ISO国家代码
 */
data class Country(
    val name: String,
    val continent: String,
    val isoCode: String
)

/**
 * 按年份统计的全球军费数据
 * 
 * @property year 年份
 * @property globalExpenditure 全球军费总开支
 * @property continentData 各大洲军费数据
 */
data class GlobalYearlyData(
    val year: Int,
    val globalExpenditure: Double,
    val continentData: Map<String, Double>
)

/**
 * 国家军事力量对比数据
 * 
 * @property countries 参与对比的国家列表
 * @property years 年份列表
 * @property expenditureData 各国各年度军费开支数据
 */
data class ComparisonData(
    val countries: List<String>,
    val years: List<Int>,
    val expenditureData: Map<String, Map<Int, Double>>
) 