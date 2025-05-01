package com.military.visualization.di

import android.content.Context
import com.military.visualization.data.local.MilitaryDatabase
import com.military.visualization.data.local.dao.CountryDao
import com.military.visualization.data.local.dao.MilitaryDataDao
import com.military.visualization.data.repository.LocalMilitaryDataSource
import com.military.visualization.data.repository.MilitaryDataSource
import dagger.Binds
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

/**
 * 数据模块依赖注入
 */
@Module
@InstallIn(SingletonComponent::class)
object DataModule {
    
    /**
     * 提供MilitaryDatabase实例
     */
    @Provides
    @Singleton
    fun provideMilitaryDatabase(@ApplicationContext context: Context): MilitaryDatabase {
        return MilitaryDatabase.getInstance(context)
    }
    
    /**
     * 提供MilitaryDataDao实例
     */
    @Provides
    @Singleton
    fun provideMilitaryDataDao(database: MilitaryDatabase): MilitaryDataDao {
        return database.militaryDataDao()
    }
    
    /**
     * 提供CountryDao实例
     */
    @Provides
    @Singleton
    fun provideCountryDao(database: MilitaryDatabase): CountryDao {
        return database.countryDao()
    }
    
    /**
     * 绑定MilitaryDataSource接口到LocalMilitaryDataSource实现
     */
    @Module
    @InstallIn(SingletonComponent::class)
    interface BindModule {
        
        @Binds
        @Singleton
        fun bindMilitaryDataSource(impl: LocalMilitaryDataSource): MilitaryDataSource
    }
} 