package com.military.visualization

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.navigation.compose.rememberNavController
import com.military.visualization.ui.navigation.MilitaryNavHost
import com.military.visualization.ui.navigation.bottomNavigation.BottomNavigationBar
import com.military.visualization.ui.theme.MilitaryVisualizationTheme
import dagger.hilt.android.AndroidEntryPoint

/**
 * 主活动
 * 作为应用程序的入口点
 */
@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MilitaryVisualizationTheme {
                // 创建导航控制器
                val navController = rememberNavController()
                
                // 创建主界面
                Scaffold(
                    bottomBar = {
                        BottomNavigationBar(navController = navController)
                    }
                ) { paddingValues ->
                    Surface(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(paddingValues)
                    ) {
                        // 导航主机
                        MilitaryNavHost(navController = navController)
                    }
                }
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun MainScreenPreview() {
    MilitaryVisualizationTheme {
        val navController = rememberNavController()
        
        Scaffold(
            bottomBar = {
                BottomNavigationBar(navController = navController)
            }
        ) { paddingValues ->
            Surface(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
            ) {
                MilitaryNavHost(navController = navController)
            }
        }
    }
} 