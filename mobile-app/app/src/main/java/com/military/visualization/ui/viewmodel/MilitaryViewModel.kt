package com.military.visualization.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.military.visualization.data.model.ComparisonData
import com.military.visualization.data.model.Country
import com.military.visualization.data.model.GlobalYearlyData
import com.military.visualization.data.model.MilitaryData
import com.military.visualization.data.repository.MilitaryDataSource
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * 军事数据ViewModel
 * 处理军事数据相关的UI逻辑
 */
@HiltViewModel
class MilitaryViewModel @Inject constructor(
    private val militaryDataSource: MilitaryDataSource
) : ViewModel() {
    
    // 当前选中的年份
    private val _selectedYear = MutableStateFlow(2022)
    val selectedYear: StateFlow<Int> = _selectedYear.asStateFlow()
    
    // 当前选中的国家
    private val _selectedCountries = MutableStateFlow<List<String>>(emptyList())
    val selectedCountries: StateFlow<List<String>> = _selectedCountries.asStateFlow()
    
    // 年份范围
    private val _yearRange = MutableStateFlow(Pair(1960, 2022))
    val yearRange: StateFlow<Pair<Int, Int>> = _yearRange.asStateFlow()
    
    // 加载状态
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()
    
    // 错误信息
    private val _errorMessage = MutableStateFlow<String?>(null)
    val errorMessage: StateFlow<String?> = _errorMessage.asStateFlow()
    
    // 数据加载状态
    private val _isDataLoaded = MutableStateFlow(false)
    val isDataLoaded: StateFlow<Boolean> = _isDataLoaded.asStateFlow()
    
    init {
        // 初始化时加载数据
        loadInitialData()
    }
    
    /**
     * 加载初始数据
     */
    private fun loadInitialData() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                // 刷新本地数据库
                militaryDataSource.refreshData()
                    .onSuccess {
                        _isDataLoaded.value = true
                    }
                    .onFailure { error ->
                        _errorMessage.value = "加载数据失败：${error.message}"
                    }
            } catch (e: Exception) {
                _errorMessage.value = "加载数据失败：${e.message}"
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    /**
     * 手动刷新数据
     */
    fun refreshData() {
        viewModelScope.launch {
            _isLoading.value = true
            _errorMessage.value = null
            
            try {
                militaryDataSource.refreshData()
                    .onSuccess {
                        _isDataLoaded.value = true
                    }
                    .onFailure { error ->
                        _errorMessage.value = "刷新数据失败：${error.message}"
                    }
            } catch (e: Exception) {
                _errorMessage.value = "刷新数据失败：${e.message}"
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    /**
     * 设置选中的年份
     */
    fun setSelectedYear(year: Int) {
        _selectedYear.value = year
    }
    
    /**
     * 设置选中的国家
     */
    fun setSelectedCountries(countries: List<String>) {
        _selectedCountries.value = countries
    }
    
    /**
     * 添加选中的国家
     */
    fun addSelectedCountry(country: String) {
        val currentList = _selectedCountries.value.toMutableList()
        if (!currentList.contains(country)) {
            currentList.add(country)
            _selectedCountries.value = currentList
        }
    }
    
    /**
     * 移除选中的国家
     */
    fun removeSelectedCountry(country: String) {
        val currentList = _selectedCountries.value.toMutableList()
        currentList.remove(country)
        _selectedCountries.value = currentList
    }
    
    /**
     * 设置年份范围
     */
    fun setYearRange(startYear: Int, endYear: Int) {
        _yearRange.value = Pair(startYear, endYear)
    }
    
    /**
     * 获取所有国家
     */
    fun getCountries(): Flow<List<Country>> {
        return militaryDataSource.getCountries()
            .catch { error ->
                _errorMessage.value = "获取国家列表失败：${error.message}"
            }
    }
    
    /**
     * 根据大洲获取国家
     */
    fun getCountriesByContinent(continent: String): Flow<List<Country>> {
        return militaryDataSource.getCountriesByContinent(continent)
            .catch { error ->
                _errorMessage.value = "获取国家列表失败：${error.message}"
            }
    }
    
    /**
     * 获取指定年份的军事数据
     */
    fun getMilitaryDataByYear(year: Int = selectedYear.value): Flow<List<MilitaryData>> {
        return militaryDataSource.getMilitaryDataByYear(year)
            .catch { error ->
                _errorMessage.value = "获取军事数据失败：${error.message}"
            }
    }
    
    /**
     * 获取指定年份军费开支最高的前N个国家
     */
    fun getTopCountriesByExpenditure(year: Int = selectedYear.value, limit: Int = 20): Flow<List<MilitaryData>> {
        return militaryDataSource.getTopCountriesByExpenditure(year, limit)
            .catch { error ->
                _errorMessage.value = "获取军费排名数据失败：${error.message}"
            }
    }
    
    /**
     * 获取国家间军事力量对比数据
     */
    suspend fun getComparisonData(
        countries: List<String> = selectedCountries.value,
        startYear: Int = yearRange.value.first,
        endYear: Int = yearRange.value.second
    ): ComparisonData {
        return try {
            militaryDataSource.getComparisonData(countries, startYear, endYear)
        } catch (e: Exception) {
            _errorMessage.value = "获取对比数据失败：${e.message}"
            ComparisonData(countries, emptyList(), emptyMap())
        }
    }
    
    /**
     * 获取全球军费年度数据
     */
    fun getGlobalYearlyData(
        startYear: Int = yearRange.value.first,
        endYear: Int = yearRange.value.second
    ): Flow<List<GlobalYearlyData>> {
        return militaryDataSource.getGlobalYearlyData(startYear, endYear)
            .catch { error ->
                _errorMessage.value = "获取全球军费数据失败：${error.message}"
            }
    }
    
    /**
     * 清除错误信息
     */
    fun clearError() {
        _errorMessage.value = null
    }
} 