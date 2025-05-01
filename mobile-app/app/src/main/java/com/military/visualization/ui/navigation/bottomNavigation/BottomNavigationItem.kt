package com.military.visualization.ui.navigation.bottomNavigation

import androidx.annotation.StringRes
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.BarChart
import androidx.compose.material.icons.filled.Compare
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Map
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.outlined.BarChart
import androidx.compose.material.icons.outlined.Compare
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.Map
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.ui.graphics.vector.ImageVector
import com.military.visualization.R
import com.military.visualization.ui.navigation.NavigationRoute

/**
 * 底部导航项
 * 定义底部导航栏中的各个选项
 */
sealed class BottomNavigationItem(
    val route: String,
    @StringRes val titleResId: Int,
    val selectedIcon: ImageVector,
    val unselectedIcon: ImageVector
) {
    // 首页
    object Home : BottomNavigationItem(
        route = NavigationRoute.Home.route,
        titleResId = R.string.bottom_nav_home,
        selectedIcon = Icons.Filled.Home,
        unselectedIcon = Icons.Outlined.Home
    )
    
    // 地图页
    object Map : BottomNavigationItem(
        route = NavigationRoute.Map.route,
        titleResId = R.string.bottom_nav_map,
        selectedIcon = Icons.Filled.Map,
        unselectedIcon = Icons.Outlined.Map
    )
    
    // 对比页
    object Comparison : BottomNavigationItem(
        route = NavigationRoute.Comparison.route,
        titleResId = R.string.bottom_nav_comparison,
        selectedIcon = Icons.Filled.Compare,
        unselectedIcon = Icons.Outlined.Compare
    )
    
    // 趋势页
    object Trends : BottomNavigationItem(
        route = NavigationRoute.Trends.route,
        titleResId = R.string.bottom_nav_trends,
        selectedIcon = Icons.Filled.BarChart,
        unselectedIcon = Icons.Outlined.BarChart
    )
    
    // 设置页
    object Settings : BottomNavigationItem(
        route = NavigationRoute.Settings.route,
        titleResId = R.string.bottom_nav_settings,
        selectedIcon = Icons.Filled.Settings,
        unselectedIcon = Icons.Outlined.Settings
    )
} 