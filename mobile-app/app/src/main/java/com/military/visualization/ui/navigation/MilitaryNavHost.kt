package com.military.visualization.ui.navigation

import androidx.compose.runtime.Composable
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavController
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.navArgument
import com.military.visualization.ui.screens.comparison.ComparisonScreen
import com.military.visualization.ui.screens.home.HomeScreen
import com.military.visualization.ui.screens.map.MapScreen
import com.military.visualization.ui.screens.settings.SettingsScreen
import com.military.visualization.ui.screens.trends.TrendsScreen
import com.military.visualization.ui.viewmodel.MilitaryViewModel

/**
 * 军事数据应用导航宿主
 * 管理不同屏幕之间的导航
 */
@Composable
fun MilitaryNavHost(navController: NavHostController) {
    // 共享的ViewModel
    val militaryViewModel: MilitaryViewModel = hiltViewModel()
    
    NavHost(
        navController = navController,
        startDestination = NavigationRoute.Home.route
    ) {
        // 主页
        composable(route = NavigationRoute.Home.route) {
            HomeScreen(
                navController = navController,
                viewModel = militaryViewModel
            )
        }
        
        // 地图页
        composable(route = NavigationRoute.Map.route) {
            MapScreen(
                navController = navController,
                viewModel = militaryViewModel
            )
        }
        
        // 对比页
        composable(route = NavigationRoute.Comparison.route) {
            ComparisonScreen(
                navController = navController,
                viewModel = militaryViewModel
            )
        }
        
        // 趋势页
        composable(route = NavigationRoute.Trends.route) {
            TrendsScreen(
                navController = navController,
                viewModel = militaryViewModel
            )
        }
        
        // 设置页
        composable(route = NavigationRoute.Settings.route) {
            SettingsScreen(
                navController = navController,
                viewModel = militaryViewModel
            )
        }
        
        // 国家详情页
        composable(
            route = NavigationRoute.CountryDetail.route,
            arguments = listOf(navArgument("countryName") { type = NavType.StringType })
        ) { backStackEntry ->
            val countryName = backStackEntry.arguments?.getString("countryName") ?: ""
            CountryDetailScreen(
                countryName = countryName,
                navController = navController,
                viewModel = militaryViewModel
            )
        }
        
        // 保存的对比页
        composable(route = NavigationRoute.SavedComparisons.route) {
            SavedComparisonsScreen(
                navController = navController,
                viewModel = militaryViewModel
            )
        }
        
        // 年度排名页
        composable(route = NavigationRoute.YearlyRankings.route) {
            YearlyRankingsScreen(
                navController = navController,
                viewModel = militaryViewModel
            )
        }
        
        // 大洲概览页
        composable(route = NavigationRoute.ContinentOverview.route) {
            ContinentOverviewScreen(
                navController = navController,
                viewModel = militaryViewModel
            )
        }
    }
}

// 以下是各个页面的临时占位实现，后续会被真正的实现替换

@Composable
fun CountryDetailScreen(
    countryName: String,
    navController: NavController,
    viewModel: MilitaryViewModel
) {
    // 临时占位，后续会实现具体内容
}

@Composable
fun SavedComparisonsScreen(
    navController: NavController,
    viewModel: MilitaryViewModel
) {
    // 临时占位，后续会实现具体内容
}

@Composable
fun YearlyRankingsScreen(
    navController: NavController,
    viewModel: MilitaryViewModel
) {
    // 临时占位，后续会实现具体内容
}

@Composable
fun ContinentOverviewScreen(
    navController: NavController,
    viewModel: MilitaryViewModel
) {
    // 临时占位，后续会实现具体内容
} 