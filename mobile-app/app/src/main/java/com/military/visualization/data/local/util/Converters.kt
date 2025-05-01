package com.military.visualization.data.local.util

import androidx.room.TypeConverter
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import java.util.Date

/**
 * Room数据库类型转换器
 */
class Converters {
    
    private val gson = Gson()
    
    /**
     * 将Long转换为Date
     */
    @TypeConverter
    fun fromTimestamp(value: Long?): Date? {
        return value?.let { Date(it) }
    }
    
    /**
     * 将Date转换为Long
     */
    @TypeConverter
    fun dateToTimestamp(date: Date?): Long? {
        return date?.time
    }
    
    /**
     * 将List<String>转换为String
     */
    @TypeConverter
    fun fromStringList(value: List<String>?): String {
        return gson.toJson(value ?: emptyList<String>())
    }
    
    /**
     * 将String转换为List<String>
     */
    @TypeConverter
    fun toStringList(value: String): List<String> {
        val type = object : TypeToken<List<String>>() {}.type
        return gson.fromJson(value, type) ?: emptyList()
    }
    
    /**
     * 将List<Int>转换为String
     */
    @TypeConverter
    fun fromIntList(value: List<Int>?): String {
        return gson.toJson(value ?: emptyList<Int>())
    }
    
    /**
     * 将String转换为List<Int>
     */
    @TypeConverter
    fun toIntList(value: String): List<Int> {
        val type = object : TypeToken<List<Int>>() {}.type
        return gson.fromJson(value, type) ?: emptyList()
    }
    
    /**
     * 将Map<String, Double>转换为String
     */
    @TypeConverter
    fun fromStringDoubleMap(value: Map<String, Double>?): String {
        return gson.toJson(value ?: emptyMap<String, Double>())
    }
    
    /**
     * 将String转换为Map<String, Double>
     */
    @TypeConverter
    fun toStringDoubleMap(value: String): Map<String, Double> {
        val type = object : TypeToken<Map<String, Double>>() {}.type
        return gson.fromJson(value, type) ?: emptyMap()
    }
} 