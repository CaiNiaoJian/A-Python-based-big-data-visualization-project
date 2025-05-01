package com.military.visualization.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Transaction
import com.military.visualization.data.local.entity.CountryEntity
import com.military.visualization.data.local.entity.MilitaryDataEntity
import kotlinx.coroutines.flow.Flow

/**
 * 军事数据DAO接口
 * 用于操作Room数据库中的军事数据表
 */
@Dao
interface MilitaryDataDao {
    
    /**
     * 插入或更新军事数据
     */
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOrUpdateMilitaryData(data: MilitaryDataEntity): Long
    
    /**
     * 批量插入或更新军事数据
     */
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOrUpdateMilitaryDataList(dataList: List<MilitaryDataEntity>): List<Long>
    
    /**
     * 根据国家和年份查询军事数据
     */
    @Query("SELECT * FROM military_data WHERE country = :country AND year = :year")
    suspend fun getMilitaryData(country: String, year: Int): MilitaryDataEntity?
    
    /**
     * 查询所有军事数据
     */
    @Query("SELECT * FROM military_data ORDER BY country, year")
    fun getAllMilitaryData(): Flow<List<MilitaryDataEntity>>
    
    /**
     * 查询指定国家的所有军事数据
     */
    @Query("SELECT * FROM military_data WHERE country = :country ORDER BY year")
    fun getMilitaryDataByCountry(country: String): Flow<List<MilitaryDataEntity>>
    
    /**
     * 查询指定年份的所有军事数据
     */
    @Query("SELECT * FROM military_data WHERE year = :year ORDER BY country")
    fun getMilitaryDataByYear(year: Int): Flow<List<MilitaryDataEntity>>
    
    /**
     * 查询指定年份范围的军事数据
     */
    @Query("SELECT * FROM military_data WHERE year BETWEEN :startYear AND :endYear ORDER BY country, year")
    fun getMilitaryDataByYearRange(startYear: Int, endYear: Int): Flow<List<MilitaryDataEntity>>
    
    /**
     * 查询指定国家和年份范围的军事数据
     */
    @Query("SELECT * FROM military_data WHERE country = :country AND year BETWEEN :startYear AND :endYear ORDER BY year")
    fun getMilitaryDataByCountryAndYearRange(country: String, startYear: Int, endYear: Int): Flow<List<MilitaryDataEntity>>
    
    /**
     * 查询指定年份军费开支最高的前N个国家
     */
    @Query("SELECT * FROM military_data WHERE year = :year ORDER BY expenditure DESC LIMIT :limit")
    fun getTopCountriesByExpenditure(year: Int, limit: Int): Flow<List<MilitaryDataEntity>>
    
    /**
     * 删除所有军事数据
     */
    @Query("DELETE FROM military_data")
    suspend fun deleteAllMilitaryData()
    
    /**
     * 删除指定国家的军事数据
     */
    @Query("DELETE FROM military_data WHERE country = :country")
    suspend fun deleteMilitaryDataByCountry(country: String)
}

/**
 * 国家信息DAO接口
 */
@Dao
interface CountryDao {
    
    /**
     * 插入或更新国家信息
     */
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOrUpdateCountry(country: CountryEntity): Long
    
    /**
     * 批量插入或更新国家信息
     */
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOrUpdateCountries(countries: List<CountryEntity>): List<Long>
    
    /**
     * 查询所有国家信息
     */
    @Query("SELECT * FROM countries ORDER BY name")
    fun getAllCountries(): Flow<List<CountryEntity>>
    
    /**
     * 根据大洲查询国家信息
     */
    @Query("SELECT * FROM countries WHERE continent = :continent ORDER BY name")
    fun getCountriesByContinent(continent: String): Flow<List<CountryEntity>>
    
    /**
     * 根据国家名称查询国家信息
     */
    @Query("SELECT * FROM countries WHERE name = :name")
    suspend fun getCountryByName(name: String): CountryEntity?
    
    /**
     * 根据ISO代码查询国家信息
     */
    @Query("SELECT * FROM countries WHERE isoCode = :isoCode")
    suspend fun getCountryByIsoCode(isoCode: String): CountryEntity?
    
    /**
     * 删除所有国家信息
     */
    @Query("DELETE FROM countries")
    suspend fun deleteAllCountries()
} 