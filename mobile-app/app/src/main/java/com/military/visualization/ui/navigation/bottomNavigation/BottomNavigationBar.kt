package com.military.visualization.ui.navigation.bottomNavigation

import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.navigation.NavController
import androidx.navigation.compose.currentBackStackEntryAsState
import com.military.visualization.ui.navigation.NavigationRoute

/**
 * 底部导航栏
 * 用于在主要页面间切换
 */
@Composable
fun BottomNavigationBar(navController: NavController) {
    // 获取底部导航项
    val items = listOf(
        BottomNavigationItem.Home,
        BottomNavigationItem.Map,
        BottomNavigationItem.Comparison,
        BottomNavigationItem.Trends,
        BottomNavigationItem.Settings
    )
    
    // 获取当前选中的导航项
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route
    
    // 创建底部导航栏
    NavigationBar(
        containerColor = MaterialTheme.colorScheme.surface,
        contentColor = MaterialTheme.colorScheme.onSurface
    ) {
        // 为每个导航项创建导航栏项
        items.forEach { item ->
            NavigationBarItem(
                icon = {
                    Icon(
                        imageVector = if (currentRoute == item.route) item.selectedIcon else item.unselectedIcon,
                        contentDescription = stringResource(id = item.titleResId)
                    )
                },
                label = { Text(text = stringResource(id = item.titleResId)) },
                selected = currentRoute == item.route,
                onClick = {
                    // 避免重复点击当前路由
                    if (currentRoute != item.route) {
                        // 导航到选中的路由
                        navController.navigate(item.route) {
                            // 弹出到起始目的地，以避免返回栈中堆积太多目的地
                            popUpTo(navController.graph.startDestinationId) {
                                saveState = true
                            }
                            // 避免重复创建相同目的地
                            launchSingleTop = true
                            // 恢复之前保存的状态
                            restoreState = true
                        }
                    }
                },
                colors = NavigationBarItemDefaults.colors(
                    selectedIconColor = MaterialTheme.colorScheme.primary,
                    selectedTextColor = MaterialTheme.colorScheme.primary,
                    unselectedIconColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f),
                    unselectedTextColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f),
                    indicatorColor = Color.Transparent
                )
            )
        }
    }
} 