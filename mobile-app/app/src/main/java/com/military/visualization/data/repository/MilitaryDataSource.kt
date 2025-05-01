package com.military.visualization.data.repository

import com.military.visualization.data.model.ComparisonData
import com.military.visualization.data.model.Country
import com.military.visualization.data.model.GlobalYearlyData
import com.military.visualization.data.model.MilitaryData
import kotlinx.coroutines.flow.Flow

/**
 * 军事数据源接口
 * 定义数据访问方法
 */
interface MilitaryDataSource {
    
    /**
     * 获取所有国家列表
     */
    fun getCountries(): Flow<List<Country>>
    
    /**
     * 根据大洲获取国家列表
     */
    fun getCountriesByContinent(continent: String): Flow<List<Country>>
    
    /**
     * 获取所有军事数据
     */
    fun getAllMilitaryData(): Flow<List<MilitaryData>>
    
    /**
     * 获取指定国家的军事数据
     */
    fun getMilitaryDataByCountry(country: String): Flow<List<MilitaryData>>
    
    /**
     * 获取指定年份的军事数据
     */
    fun getMilitaryDataByYear(year: Int): Flow<List<MilitaryData>>
    
    /**
     * 获取指定年份范围的军事数据
     */
    fun getMilitaryDataByYearRange(startYear: Int, endYear: Int): Flow<List<MilitaryData>>
    
    /**
     * 获取指定国家和年份范围的军事数据
     */
    fun getMilitaryDataByCountryAndYearRange(country: String, startYear: Int, endYear: Int): Flow<List<MilitaryData>>
    
    /**
     * 获取指定年份军费开支最高的前N个国家
     */
    fun getTopCountriesByExpenditure(year: Int, limit: Int): Flow<List<MilitaryData>>
    
    /**
     * 获取国家间军事力量对比数据
     */
    suspend fun getComparisonData(countries: List<String>, startYear: Int, endYear: Int): ComparisonData
    
    /**
     * 获取全球军费年度数据
     */
    fun getGlobalYearlyData(startYear: Int, endYear: Int): Flow<List<GlobalYearlyData>>
    
    /**
     * 刷新数据（从远程数据源获取最新数据）
     */
    suspend fun refreshData(): Result<Boolean>
    
    /**
     * 刷新国家数据
     */
    suspend fun refreshCountries(): Result<Boolean>
    
    /**
     * 刷新军事数据
     */
    suspend fun refreshMilitaryData(forceRefresh: Boolean = false): Result<Boolean>
} 