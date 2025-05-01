package com.military.visualization.ui.screens.home

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.BarChart
import androidx.compose.material.icons.filled.Map
import androidx.compose.material.icons.filled.Public
import androidx.compose.material.icons.filled.ShowChart
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.military.visualization.R
import com.military.visualization.ui.components.DataCard
import com.military.visualization.ui.components.ErrorView
import com.military.visualization.ui.components.LoadingView
import com.military.visualization.ui.components.MilitaryTopBar
import com.military.visualization.ui.navigation.NavigationRoute
import com.military.visualization.ui.viewmodel.MilitaryViewModel

/**
 * 首页屏幕
 * 应用的主要入口
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    navController: NavController,
    viewModel: MilitaryViewModel
) {
    // 从ViewModel获取状态
    val isLoading by viewModel.isLoading.collectAsState()
    val errorMessage by viewModel.errorMessage.collectAsState()
    val isDataLoaded by viewModel.isDataLoaded.collectAsState()
    
    // 加载数据
    LaunchedEffect(key1 = Unit) {
        if (!isDataLoaded) {
            viewModel.refreshData()
        }
    }
    
    // 创建界面
    Scaffold(
        topBar = {
            MilitaryTopBar(
                title = stringResource(id = R.string.home_title),
                showSearch = true,
                onSearchClick = {
                    // 待实现：搜索功能
                }
            )
        }
    ) { paddingValues ->
        if (isLoading) {
            LoadingView()
        } else if (errorMessage != null) {
            ErrorView(
                message = errorMessage ?: "未知错误",
                onRetry = { viewModel.refreshData() }
            )
        } else {
            HomeContent(
                paddingValues = paddingValues,
                navController = navController
            )
        }
    }
}

/**
 * 首页内容
 */
@Composable
private fun HomeContent(
    paddingValues: PaddingValues,
    navController: NavController
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(paddingValues)
            .verticalScroll(rememberScrollState())
    ) {
        // 欢迎标题
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 24.dp)
        ) {
            Text(
                text = stringResource(id = R.string.home_title),
                style = MaterialTheme.typography.headlineMedium
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = stringResource(id = R.string.home_subtitle),
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
            )
            
            // 数据来源信息
            Spacer(modifier = Modifier.height(16.dp))
            Text(
                text = stringResource(id = R.string.data_source),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f),
                textAlign = TextAlign.Center,
                modifier = Modifier.fillMaxWidth()
            )
        }
        
        // 功能卡片
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // 世界地图
            DataCard(
                title = stringResource(id = R.string.bottom_nav_map),
                subtitle = "查看全球军事力量分布",
                icon = Icons.Default.Map,
                onClick = {
                    navController.navigate(NavigationRoute.Map.route)
                }
            )
            
            // 军费排名
            DataCard(
                title = stringResource(id = R.string.home_top_countries),
                subtitle = "探索各国军费开支排名",
                icon = Icons.Default.ShowChart,
                onClick = {
                    navController.navigate(NavigationRoute.YearlyRankings.route)
                }
            )
            
            // 国家对比
            DataCard(
                title = stringResource(id = R.string.bottom_nav_comparison),
                subtitle = "对比不同国家的军事力量",
                icon = Icons.Default.BarChart,
                onClick = {
                    navController.navigate(NavigationRoute.Comparison.route)
                }
            )
            
            // 大洲概览
            DataCard(
                title = stringResource(id = R.string.home_continent_overview),
                subtitle = "按大洲查看军事力量分布",
                icon = Icons.Default.Public,
                onClick = {
                    navController.navigate(NavigationRoute.ContinentOverview.route)
                }
            )
        }
    }
} 