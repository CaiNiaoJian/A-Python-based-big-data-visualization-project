package com.military.visualization.ui.screens.comparison

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.Button
import androidx.compose.material3.Divider
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
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
import com.military.visualization.ui.components.EmptyView
import com.military.visualization.ui.components.ErrorView
import com.military.visualization.ui.components.LoadingView
import com.military.visualization.ui.components.MilitaryTopBar
import com.military.visualization.ui.components.YearSelector
import com.military.visualization.ui.viewmodel.MilitaryViewModel

/**
 * 对比屏幕
 * 用于对比不同国家的军事数据
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ComparisonScreen(
    navController: NavController,
    viewModel: MilitaryViewModel
) {
    // 从ViewModel获取状态
    val isLoading by viewModel.isLoading.collectAsState()
    val error by viewModel.error.collectAsState()
    val hasData by viewModel.hasData.collectAsState()
    val selectedYear by viewModel.selectedYear.collectAsState()
    
    // 本地状态
    var selectedCountries by remember { mutableStateOf(listOf<String>()) }
    
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
                title = stringResource(id = R.string.comparison_title),
                showSearch = true,
                onSearchClick = { /* 待实现 */ }
            )
        }
    ) { paddingValues ->
        when {
            isLoading && !hasData -> LoadingView()
            error != null -> ErrorView(
                message = error ?: stringResource(id = R.string.error_loading),
                onRetry = { viewModel.refreshData() }
            )
            else -> ComparisonContent(
                paddingValues = paddingValues,
                selectedYear = selectedYear,
                onYearChanged = { viewModel.updateSelectedYear(it) },
                selectedCountries = selectedCountries,
                onAddCountry = { country ->
                    if (!selectedCountries.contains(country) && selectedCountries.size < 5) {
                        selectedCountries = selectedCountries + country
                    }
                },
                onRemoveCountry = { country ->
                    selectedCountries = selectedCountries.filter { it != country }
                },
                onNavigateToCountrySelection = {
                    // 待实现：导航到国家选择
                }
            )
        }
    }
}

/**
 * 对比内容
 */
@Composable
private fun ComparisonContent(
    paddingValues: PaddingValues,
    selectedYear: Int,
    onYearChanged: (Int) -> Unit,
    selectedCountries: List<String>,
    onAddCountry: (String) -> Unit,
    onRemoveCountry: (String) -> Unit,
    onNavigateToCountrySelection: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(paddingValues)
            .verticalScroll(rememberScrollState())
    ) {
        // 年份选择器
        YearSelector(
            initialYear = selectedYear,
            minYear = 2000,
            maxYear = 2023,
            onYearChanged = onYearChanged,
            modifier = Modifier.padding(16.dp)
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // 选中的国家列表
        if (selectedCountries.isEmpty()) {
            EmptyCountriesView(onNavigateToCountrySelection)
        } else {
            SelectedCountriesView(
                selectedCountries = selectedCountries,
                onRemoveCountry = onRemoveCountry,
                onAddCountry = onNavigateToCountrySelection
            )
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // 假数据图表（仅作为占位符）
            ComparisonChartPlaceholder()
        }
    }
}

/**
 * 无选中国家视图
 */
@Composable
private fun EmptyCountriesView(onNavigateToCountrySelection: () -> Unit) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(200.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = stringResource(id = R.string.comparison_empty),
                style = MaterialTheme.typography.bodyLarge,
                textAlign = TextAlign.Center
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Button(onClick = onNavigateToCountrySelection) {
                Icon(
                    imageVector = Icons.Default.Add,
                    contentDescription = null
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text(text = stringResource(id = R.string.comparison_add_country))
            }
        }
    }
}

/**
 * 已选中国家列表
 */
@Composable
private fun SelectedCountriesView(
    selectedCountries: List<String>,
    onRemoveCountry: (String) -> Unit,
    onAddCountry: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp)
    ) {
        Text(
            text = stringResource(id = R.string.comparison_selected_countries),
            style = MaterialTheme.typography.titleMedium,
            modifier = Modifier.padding(bottom = 8.dp)
        )
        
        Divider()
        
        // 已选择的国家列表
        selectedCountries.forEach { country ->
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = country,
                    style = MaterialTheme.typography.bodyLarge,
                    modifier = Modifier.weight(1f)
                )
                IconButton(onClick = { onRemoveCountry(country) }) {
                    Icon(
                        imageVector = Icons.Default.Close,
                        contentDescription = stringResource(id = R.string.remove)
                    )
                }
            }
            Divider()
        }
        
        // 添加更多国家按钮
        if (selectedCountries.size < 5) {
            OutlinedButton(
                onClick = onAddCountry,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 8.dp)
            ) {
                Icon(
                    imageVector = Icons.Default.Add,
                    contentDescription = null
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text(text = stringResource(id = R.string.comparison_add_more))
            }
        }
    }
}

/**
 * 数据对比图表占位符
 */
@Composable
private fun ComparisonChartPlaceholder() {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(300.dp)
            .padding(16.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = stringResource(id = R.string.comparison_chart_placeholder),
            style = MaterialTheme.typography.bodyLarge,
            textAlign = TextAlign.Center
        )
    }
} 