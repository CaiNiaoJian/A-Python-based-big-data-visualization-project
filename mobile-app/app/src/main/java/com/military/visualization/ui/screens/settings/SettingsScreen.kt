package com.military.visualization.ui.screens.settings

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
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
import com.military.visualization.ui.components.MilitaryTopBar
import com.military.visualization.ui.viewmodel.MilitaryViewModel

/**
 * 设置屏幕
 * 用户可以在此修改应用设置
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    navController: NavController,
    viewModel: MilitaryViewModel
) {
    // 从ViewModel获取状态
    val isLoading by viewModel.isLoading.collectAsState()
    
    // 创建设置状态
    var selectedTheme by remember { mutableStateOf("system") }
    var selectedLanguage by remember { mutableStateOf("system") }
    
    // 创建界面
    Scaffold(
        topBar = {
            MilitaryTopBar(
                title = stringResource(id = R.string.settings_title)
            )
        }
    ) { paddingValues ->
        SettingsContent(
            paddingValues = paddingValues,
            selectedTheme = selectedTheme,
            selectedLanguage = selectedLanguage,
            onThemeSelected = { selectedTheme = it },
            onLanguageSelected = { selectedLanguage = it },
            onClearCache = {
                // 待实现：清除缓存功能
            },
            onRefreshData = {
                viewModel.refreshData()
            },
            isLoading = isLoading
        )
    }
}

/**
 * 设置内容
 */
@Composable
private fun SettingsContent(
    paddingValues: PaddingValues,
    selectedTheme: String,
    selectedLanguage: String,
    onThemeSelected: (String) -> Unit,
    onLanguageSelected: (String) -> Unit,
    onClearCache: () -> Unit,
    onRefreshData: () -> Unit,
    isLoading: Boolean
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(paddingValues)
            .verticalScroll(rememberScrollState())
    ) {
        // 主题设置
        SettingSection(
            title = stringResource(id = R.string.settings_theme),
            options = listOf(
                stringResource(id = R.string.settings_theme_light) to "light",
                stringResource(id = R.string.settings_theme_dark) to "dark",
                stringResource(id = R.string.settings_theme_system) to "system"
            ),
            selectedOption = selectedTheme,
            onOptionSelected = onThemeSelected
        )
        
        // 语言设置
        SettingSection(
            title = stringResource(id = R.string.settings_language),
            options = listOf(
                stringResource(id = R.string.settings_language_zh) to "zh",
                stringResource(id = R.string.settings_language_en) to "en",
                stringResource(id = R.string.settings_language_system) to "system"
            ),
            selectedOption = selectedLanguage,
            onOptionSelected = onLanguageSelected
        )
        
        // 数据操作
        SettingActionItems(
            onClearCache = onClearCache,
            onRefreshData = onRefreshData,
            isLoading = isLoading
        )
        
        // 关于应用
        AboutSection()
    }
}

/**
 * 设置项分组
 */
@Composable
private fun SettingSection(
    title: String,
    options: List<Pair<String, String>>,
    selectedOption: String,
    onOptionSelected: (String) -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = title,
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            options.forEach { (text, value) ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .selectable(
                            selected = (value == selectedOption),
                            onClick = { onOptionSelected(value) }
                        )
                        .padding(vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    RadioButton(
                        selected = (value == selectedOption),
                        onClick = { onOptionSelected(value) }
                    )
                    Text(
                        text = text,
                        style = MaterialTheme.typography.bodyMedium,
                        modifier = Modifier.padding(start = 8.dp)
                    )
                }
            }
        }
    }
}

/**
 * 设置操作项
 */
@Composable
private fun SettingActionItems(
    onClearCache: () -> Unit,
    onRefreshData: () -> Unit,
    isLoading: Boolean
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = stringResource(id = R.string.settings_data_management),
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Button(
                onClick = onRefreshData,
                enabled = !isLoading,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = if (isLoading) 
                        stringResource(id = R.string.loading) 
                    else 
                        stringResource(id = R.string.settings_refresh_data)
                )
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            OutlinedButton(
                onClick = onClearCache,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(text = stringResource(id = R.string.settings_clear_cache))
            }
        }
    }
}

/**
 * 关于部分
 */
@Composable
private fun AboutSection() {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = stringResource(id = R.string.settings_about),
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Text(
                text = stringResource(id = R.string.app_name),
                style = MaterialTheme.typography.titleLarge,
                textAlign = TextAlign.Center,
                modifier = Modifier.fillMaxWidth()
            )
            
            Spacer(modifier = Modifier.height(4.dp))
            
            Text(
                text = "版本 1.0.0",
                style = MaterialTheme.typography.bodyMedium,
                textAlign = TextAlign.Center,
                modifier = Modifier.fillMaxWidth()
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Text(
                text = "© 2023 军事数据可视化项目团队",
                style = MaterialTheme.typography.bodySmall,
                textAlign = TextAlign.Center,
                modifier = Modifier.fillMaxWidth()
            )
        }
    }
} 