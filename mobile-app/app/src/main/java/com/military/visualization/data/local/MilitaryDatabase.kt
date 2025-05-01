package com.military.visualization.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.military.visualization.data.local.dao.CountryDao
import com.military.visualization.data.local.dao.MilitaryDataDao
import com.military.visualization.data.local.entity.CountryEntity
import com.military.visualization.data.local.entity.MilitaryDataEntity
import com.military.visualization.data.local.util.Converters

/**
 * 军事数据库
 * 用于管理Room数据库
 */
@Database(
    entities = [
        MilitaryDataEntity::class,
        CountryEntity::class
    ],
    version = 1,
    exportSchema = false
)
@TypeConverters(Converters::class)
abstract class MilitaryDatabase : RoomDatabase() {
    
    /**
     * 获取军事数据DAO
     */
    abstract fun militaryDataDao(): MilitaryDataDao
    
    /**
     * 获取国家信息DAO
     */
    abstract fun countryDao(): CountryDao
    
    companion object {
        private const val DATABASE_NAME = "military_database"
        
        @Volatile
        private var INSTANCE: MilitaryDatabase? = null
        
        /**
         * 获取数据库实例
         */
        fun getInstance(context: Context): MilitaryDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    MilitaryDatabase::class.java,
                    DATABASE_NAME
                )
                .fallbackToDestructiveMigration() // 如果数据库版本升级，简单重建表
                .build()
                
                INSTANCE = instance
                instance
            }
        }
    }
} 