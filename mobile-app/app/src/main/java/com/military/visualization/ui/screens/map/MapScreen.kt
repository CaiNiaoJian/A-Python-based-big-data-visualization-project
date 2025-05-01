package com.military.visualization.ui.screens.map

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
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
 * 地图屏幕
 * 展示军事数据的地理分布
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MapScreen(
    navController: NavController,
    viewModel: MilitaryViewModel
) {
    // 从ViewModel获取状态
    val isLoading by viewModel.isLoading.collectAsState()
    val error by viewModel.error.collectAsState()
    val hasData by viewModel.hasData.collectAsState()
    val selectedYear by viewModel.selectedYear.collectAsState()
    
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
                title = stringResource(id = R.string.map_title),
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
            else -> MapContent(
                paddingValues = paddingValues,
                selectedYear = selectedYear,
                onYearChanged = { viewModel.updateSelectedYear(it) }
            )
        }
    }
}

/**
 * 地图内容
 */
@Composable
private fun MapContent(
    paddingValues: PaddingValues,
    selectedYear: Int,
    onYearChanged: (Int) -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(paddingValues)
    ) {
        // 年份选择器
        YearSelector(
            initialYear = selectedYear,
            minYear = 2000,
            maxYear = 2023,
            onYearChanged = onYearChanged,
            modifier = Modifier.padding(16.dp)
        )
        
        // 地图视图（暂时使用占位符）
        Box(
            modifier = Modifier
                .fillMaxSize()
                .weight(1f),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = stringResource(id = R.string.map_placeholder),
                style = MaterialTheme.typography.bodyLarge
            )
        }
    }
} 