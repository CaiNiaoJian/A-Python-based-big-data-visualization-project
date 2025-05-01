package com.military.visualization.data.repository

import com.military.visualization.data.local.dao.CountryDao
import com.military.visualization.data.local.dao.MilitaryDataDao
import com.military.visualization.data.local.entity.CountryEntity
import com.military.visualization.data.local.entity.toDomainModel
import com.military.visualization.data.loader.ExcelDataLoader
import com.military.visualization.data.model.ComparisonData
import com.military.visualization.data.model.Country
import com.military.visualization.data.model.GlobalYearlyData
import com.military.visualization.data.model.MilitaryData
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

/**
 * 本地军事数据源
 * 实现从本地数据库和资源文件获取数据
 */
@Singleton
class LocalMilitaryDataSource @Inject constructor(
    private val militaryDataDao: MilitaryDataDao,
    private val countryDao: CountryDao,
    private val excelDataLoader: ExcelDataLoader
) : MilitaryDataSource {
    
    /**
     * 获取所有国家列表
     */
    override fun getCountries(): Flow<List<Country>> {
        return countryDao.getAllCountries().map { entities ->
            entities.map { entity ->
                Country(
                    name = entity.name,
                    continent = entity.continent,
                    isoCode = entity.isoCode
                )
            }
        }
    }
    
    /**
     * 根据大洲获取国家列表
     */
    override fun getCountriesByContinent(continent: String): Flow<List<Country>> {
        return countryDao.getCountriesByContinent(continent).map { entities ->
            entities.map { entity ->
                Country(
                    name = entity.name,
                    continent = entity.continent,
                    isoCode = entity.isoCode
                )
            }
        }
    }
    
    /**
     * 获取所有军事数据
     */
    override fun getAllMilitaryData(): Flow<List<MilitaryData>> {
        return militaryDataDao.getAllMilitaryData().map { entities ->
            entities.map { it.toDomainModel() }
        }
    }
    
    /**
     * 获取指定国家的军事数据
     */
    override fun getMilitaryDataByCountry(country: String): Flow<List<MilitaryData>> {
        return militaryDataDao.getMilitaryDataByCountry(country).map { entities ->
            entities.map { it.toDomainModel() }
        }
    }
    
    /**
     * 获取指定年份的军事数据
     */
    override fun getMilitaryDataByYear(year: Int): Flow<List<MilitaryData>> {
        return militaryDataDao.getMilitaryDataByYear(year).map { entities ->
            entities.map { it.toDomainModel() }
        }
    }
    
    /**
     * 获取指定年份范围的军事数据
     */
    override fun getMilitaryDataByYearRange(startYear: Int, endYear: Int): Flow<List<MilitaryData>> {
        return militaryDataDao.getMilitaryDataByYearRange(startYear, endYear).map { entities ->
            entities.map { it.toDomainModel() }
        }
    }
    
    /**
     * 获取指定国家和年份范围的军事数据
     */
    override fun getMilitaryDataByCountryAndYearRange(country: String, startYear: Int, endYear: Int): Flow<List<MilitaryData>> {
        return militaryDataDao.getMilitaryDataByCountryAndYearRange(country, startYear, endYear).map { entities ->
            entities.map { it.toDomainModel() }
        }
    }
    
    /**
     * 获取指定年份军费开支最高的前N个国家
     */
    override fun getTopCountriesByExpenditure(year: Int, limit: Int): Flow<List<MilitaryData>> {
        return militaryDataDao.getTopCountriesByExpenditure(year, limit).map { entities ->
            entities.map { it.toDomainModel() }
        }
    }
    
    /**
     * 获取国家间军事力量对比数据
     */
    override suspend fun getComparisonData(countries: List<String>, startYear: Int, endYear: Int): ComparisonData {
        // 创建年份列表
        val years = (startYear..endYear).toList()
        
        // 初始化结果Map
        val expenditureData = mutableMapOf<String, MutableMap<Int, Double>>()
        
        // 为每个国家初始化数据
        countries.forEach { country ->
            expenditureData[country] = mutableMapOf()
        }
        
        // 查询每个国家在指定年份范围内的数据
        countries.forEach { country ->
            // 使用DAO查询数据
            militaryDataDao.getMilitaryDataByCountryAndYearRange(country, startYear, endYear)
                .map { entities ->
                    entities.map { it.toDomainModel() }
                }
                .collect { militaryDataList ->
                    // 将数据添加到结果Map
                    militaryDataList.forEach { militaryData ->
                        expenditureData[country]?.put(militaryData.year, militaryData.expenditure)
                    }
                }
        }
        
        return ComparisonData(
            countries = countries,
            years = years,
            expenditureData = expenditureData
        )
    }
    
    /**
     * 获取全球军费年度数据
     */
    override fun getGlobalYearlyData(startYear: Int, endYear: Int): Flow<List<GlobalYearlyData>> {
        // 获取指定年份范围内的数据
        return militaryDataDao.getMilitaryDataByYearRange(startYear, endYear).map { entities ->
            // 将实体转换为领域模型
            val militaryDataList = entities.map { it.toDomainModel() }
            
            // 按年份分组
            val dataByYear = militaryDataList.groupBy { it.year }
            
            // 计算每年的全球军费总开支和各大洲军费
            dataByYear.map { (year, dataList) ->
                // 计算全球军费总开支
                val globalExpenditure = dataList.sumOf { it.expenditure }
                
                // 按大洲分组并计算各大洲军费
                val continentData = mutableMapOf<String, Double>()
                
                // 查询每个国家所属的大洲
                val countryContinent = mutableMapOf<String, String>()
                countryDao.getAllCountries().map { countryEntities ->
                    countryEntities.forEach { entity ->
                        countryContinent[entity.name] = entity.continent
                    }
                }.collect()
                
                // 计算各大洲军费
                dataList.forEach { militaryData ->
                    val continent = countryContinent[militaryData.country] ?: "未知"
                    val currentExpenditure = continentData[continent] ?: 0.0
                    continentData[continent] = currentExpenditure + militaryData.expenditure
                }
                
                GlobalYearlyData(
                    year = year,
                    globalExpenditure = globalExpenditure,
                    continentData = continentData
                )
            }.sortedBy { it.year }
        }
    }
    
    /**
     * 刷新数据（从Excel文件加载数据）
     */
    override suspend fun refreshData(): Result<Boolean> {
        return try {
            refreshCountries()
            refreshMilitaryData()
            Result.success(true)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    /**
     * 刷新国家数据
     */
    override suspend fun refreshCountries(): Result<Boolean> {
        return try {
            // 从Excel文件加载国家数据
            val countries = excelDataLoader.loadAllCountries()
            
            // 转换为实体并保存到数据库
            val countryEntities = countries.map { country ->
                CountryEntity(
                    name = country.name,
                    continent = country.continent,
                    isoCode = country.isoCode
                )
            }
            
            // 保存到数据库
            countryDao.insertOrUpdateCountries(countryEntities)
            
            Result.success(true)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    /**
     * 刷新军事数据
     */
    override suspend fun refreshMilitaryData(forceRefresh: Boolean): Result<Boolean> {
        return try {
            // 检查数据库中是否已有数据
            var hasData = false
            militaryDataDao.getAllMilitaryData().collect { entities ->
                hasData = entities.isNotEmpty()
            }
            
            // 如果已有数据且不强制刷新，则跳过
            if (hasData && !forceRefresh) {
                return Result.success(false)
            }
            
            // 从Excel文件加载军事数据
            val militaryDataList = excelDataLoader.loadAllMilitaryData()
            
            // 转换为实体并保存到数据库
            val militaryDataEntities = militaryDataList.map { militaryData ->
                com.military.visualization.data.local.entity.MilitaryDataEntity(
                    country = militaryData.country,
                    year = militaryData.year,
                    expenditure = militaryData.expenditure,
                    gdpPercentage = militaryData.gdpPercentage,
                    perCapita = militaryData.perCapita
                )
            }
            
            // 保存到数据库
            militaryDataDao.insertOrUpdateMilitaryDataList(militaryDataEntities)
            
            Result.success(true)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
} 