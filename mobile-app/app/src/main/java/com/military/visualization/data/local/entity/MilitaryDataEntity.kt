package com.military.visualization.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey
import com.military.visualization.data.model.MilitaryData

/**
 * 军事数据实体类
 * 用于Room数据库存储
 */
@Entity(
    tableName = "military_data",
    indices = [
        Index(value = ["country", "year"], unique = true)
    ]
)
data class MilitaryDataEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val country: String,
    val year: Int,
    val expenditure: Double,
    val gdpPercentage: Double?,
    val perCapita: Double?,
    val lastUpdated: Long = System.currentTimeMillis()
)

/**
 * 国家信息实体类
 */
@Entity(
    tableName = "countries",
    indices = [
        Index(value = ["name"], unique = true),
        Index(value = ["isoCode"], unique = true)
    ]
)
data class CountryEntity(
    @PrimaryKey
    val isoCode: String,
    val name: String,
    val continent: String,
    val lastUpdated: Long = System.currentTimeMillis()
)

// 扩展函数：将实体类转换为领域模型
fun MilitaryDataEntity.toDomainModel(): MilitaryData {
    return MilitaryData(
        country = country,
        year = year,
        expenditure = expenditure,
        gdpPercentage = gdpPercentage,
        perCapita = perCapita
    )
}

// 扩展函数：将领域模型转换为实体类
fun MilitaryData.toEntity(): MilitaryDataEntity {
    return MilitaryDataEntity(
        country = country,
        year = year,
        expenditure = expenditure,
        gdpPercentage = gdpPercentage,
        perCapita = perCapita
    )
} 