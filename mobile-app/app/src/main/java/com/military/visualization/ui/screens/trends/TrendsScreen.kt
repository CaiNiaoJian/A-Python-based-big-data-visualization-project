package com.military.visualization.ui.screens.trends

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.military.visualization.R
import com.military.visualization.ui.components.ErrorView
import com.military.visualization.ui.components.LoadingView
import com.military.visualization.ui.components.MilitaryTopBar
import com.military.visualization.ui.components.YearRangeSelector
import com.military.visualization.ui.viewmodel.MilitaryViewModel

/**
 * 趋势屏幕
 * 展示军事数据的时间趋势
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TrendsScreen(
    navController: NavController,
    viewModel: MilitaryViewModel
) {
    // 从ViewModel获取状态
    val isLoading by viewModel.isLoading.collectAsState()
    val error by viewModel.error.collectAsState()
    val hasData by viewModel.hasData.collectAsState()
    
    // 本地状态
    var startYear by remember { mutableStateOf(2000) }
    var endYear by remember { mutableStateOf(2023) }
    var selectedCountry by remember { mutableStateOf("中国") }
    var selectedDataType by remember { mutableStateOf("军费开支") }
    var showCountryDropdown by remember { mutableStateOf(false) }
    var showDataTypeDropdown by remember { mutableStateOf(false) }
    
    // 加载数据
    LaunchedEffect(Unit) {
        if (!hasData) {
            viewModel.refreshData()
        }
    }
    
    // 创建界面
    Scaffold(
        topBar = {
            MilitaryTopBar(
                title = stringResource(id = R.string.trends_title)
            )
        }
    ) { paddingValues ->
        when {
            isLoading && !hasData -> LoadingView()
            error != null -> ErrorView(
                message = error ?: stringResource(id = R.string.error_loading),
                onRetry = { viewModel.refreshData() }
            )
            else -> TrendsContent(
                paddingValues = paddingValues,
                startYear = startYear,
                endYear = endYear,
                onYearRangeChanged = { start, end ->
                    startYear = start
                    endYear = end
                },
                selectedCountry = selectedCountry,
                onCountryClick = { showCountryDropdown = true },
                showCountryDropdown = showCountryDropdown,
                onCountryDismiss = { showCountryDropdown = false },
                onCountrySelected = { 
                    selectedCountry = it
                    showCountryDropdown = false
                },
                selectedDataType = selectedDataType,
                onDataTypeClick = { showDataTypeDropdown = true },
                showDataTypeDropdown = showDataTypeDropdown,
                onDataTypeDismiss = { showDataTypeDropdown = false },
                onDataTypeSelected = {
                    selectedDataType = it
                    showDataTypeDropdown = false
                }
            )
        }
    }
}

/**
 * 趋势内容
 */
@Composable
private fun TrendsContent(
    paddingValues: PaddingValues,
    startYear: Int,
    endYear: Int,
    onYearRangeChanged: (Int, Int) -> Unit,
    selectedCountry: String,
    onCountryClick: () -> Unit,
    showCountryDropdown: Boolean,
    onCountryDismiss: () -> Unit,
    onCountrySelected: (String) -> Unit,
    selectedDataType: String,
    onDataTypeClick: () -> Unit,
    showDataTypeDropdown: Boolean,
    onDataTypeDismiss: () -> Unit,
    onDataTypeSelected: (String) -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(paddingValues)
            .verticalScroll(rememberScrollState())
    ) {
        // 年份范围选择器
        YearRangeSelector(
            initialStartYear = startYear,
            initialEndYear = endYear,
            minYear = 2000,
            maxYear = 2023,
            onYearRangeChanged = onYearRangeChanged,
            modifier = Modifier.padding(16.dp)
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // 筛选选项
        FilterOptions(
            selectedCountry = selectedCountry,
            onCountryClick = onCountryClick,
            showCountryDropdown = showCountryDropdown,
            onCountryDismiss = onCountryDismiss,
            onCountrySelected = onCountrySelected,
            selectedDataType = selectedDataType,
            onDataTypeClick = onDataTypeClick,
            showDataTypeDropdown = showDataTypeDropdown,
            onDataTypeDismiss = onDataTypeDismiss,
            onDataTypeSelected = onDataTypeSelected
        )
        
        Spacer(modifier = Modifier.height(24.dp))
        
        // 趋势图表（占位符）
        TrendChartPlaceholder()
    }
}

/**
 * 筛选选项
 */
@Composable
private fun FilterOptions(
    selectedCountry: String,
    onCountryClick: () -> Unit,
    showCountryDropdown: Boolean,
    onCountryDismiss: () -> Unit,
    onCountrySelected: (String) -> Unit,
    selectedDataType: String,
    onDataTypeClick: () -> Unit,
    showDataTypeDropdown: Boolean,
    onDataTypeDismiss: () -> Unit,
    onDataTypeSelected: (String) -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = stringResource(id = R.string.trends_filter),
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // 国家选择
            Box(modifier = Modifier.fillMaxWidth()) {
                OutlinedButton(
                    onClick = onCountryClick,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(text = selectedCountry)
                }
                
                DropdownMenu(
                    expanded = showCountryDropdown,
                    onDismissRequest = onCountryDismiss
                ) {
                    listOf("中国", "美国", "俄罗斯", "英国", "法国", "日本", "印度").forEach { country ->
                        DropdownMenuItem(
                            text = { Text(text = country) },
                            onClick = { onCountrySelected(country) }
                        )
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            // 数据类型选择
            Box(modifier = Modifier.fillMaxWidth()) {
                OutlinedButton(
                    onClick = onDataTypeClick,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(text = selectedDataType)
                }
                
                DropdownMenu(
                    expanded = showDataTypeDropdown,
                    onDismissRequest = onDataTypeDismiss
                ) {
                    listOf("军费开支", "现役人数", "战斗机数量", "舰船数量", "坦克数量").forEach { dataType ->
                        DropdownMenuItem(
                            text = { Text(text = dataType) },
                            onClick = { onDataTypeSelected(dataType) }
                        )
                    }
                }
            }
        }
    }
}

/**
 * 趋势图表占位符
 */
@Composable
private fun TrendChartPlaceholder() {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(300.dp)
            .padding(16.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = stringResource(id = R.string.trends_chart_placeholder),
            style = MaterialTheme.typography.bodyLarge,
            textAlign = TextAlign.Center
        )
    }
} 