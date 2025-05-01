package com.military.visualization.ui.navigation

/**
 * 导航路由
 * 定义应用程序中的导航路径
 */
sealed class NavigationRoute(val route: String) {
    
    // 主要标签页路由
    object Home : NavigationRoute("home")
    object Map : NavigationRoute("map")
    object Comparison : NavigationRoute("comparison")
    object Trends : NavigationRoute("trends")
    object Settings : NavigationRoute("settings")
    
    // 详情页路由
    object CountryDetail : NavigationRoute("country_detail/{countryName}") {
        fun createRoute(countryName: String) = "country_detail/${countryName}"
    }
    
    // 子标签页路由
    object SavedComparisons : NavigationRoute("saved_comparisons")
    object YearlyRankings : NavigationRoute("yearly_rankings")
    object ContinentOverview : NavigationRoute("continent_overview")
} 