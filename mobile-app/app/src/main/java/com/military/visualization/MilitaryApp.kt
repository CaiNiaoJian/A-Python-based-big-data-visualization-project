package com.military.visualization

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

/**
 * 军事力量可视化应用程序
 * 主应用类
 */
@HiltAndroidApp
class MilitaryApp : Application() {
    
    override fun onCreate() {
        super.onCreate()
        
        // 初始化日志系统
        setupLogging()
        
        // 初始化偏好设置
        setupPreferences()
    }
    
    private fun setupLogging() {
        // 在正式版中禁用详细日志
        val isDebug = BuildConfig.DEBUG
        // 这里可以配置日志系统，例如Timber等
    }
    
    private fun setupPreferences() {
        // 初始化应用程序设置
    }
} 