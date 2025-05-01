package com.military.visualization.ui.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.KeyboardArrowLeft
import androidx.compose.material.icons.filled.KeyboardArrowRight
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
import androidx.compose.material3.SliderDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.military.visualization.R
import kotlin.math.roundToInt

/**
 * 年份选择器组件
 * 用于选择要查看的年份
 */
@Composable
fun YearSelector(
    initialYear: Int,
    minYear: Int,
    maxYear: Int,
    onYearChanged: (Int) -> Unit
) {
    // 计算初始滑块值
    val initialSliderValue = (initialYear - minYear).toFloat() / (maxYear - minYear).toFloat()
    
    // 创建状态
    var sliderValue by remember { mutableFloatStateOf(initialSliderValue) }
    var currentYear by remember { mutableStateOf(initialYear) }
    
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
    ) {
        // 年份显示和左右按钮
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = stringResource(id = R.string.year),
                style = MaterialTheme.typography.bodyLarge
            )
            Spacer(modifier = Modifier.width(8.dp))
            
            IconButton(
                onClick = {
                    if (currentYear > minYear) {
                        currentYear--
                        sliderValue = (currentYear - minYear).toFloat() / (maxYear - minYear).toFloat()
                        onYearChanged(currentYear)
                    }
                },
                enabled = currentYear > minYear
            ) {
                Icon(
                    imageVector = Icons.Filled.KeyboardArrowLeft,
                    contentDescription = "减少年份"
                )
            }
            
            Text(
                text = currentYear.toString(),
                style = MaterialTheme.typography.titleLarge,
                modifier = Modifier.padding(horizontal = 8.dp)
            )
            
            IconButton(
                onClick = {
                    if (currentYear < maxYear) {
                        currentYear++
                        sliderValue = (currentYear - minYear).toFloat() / (maxYear - minYear).toFloat()
                        onYearChanged(currentYear)
                    }
                },
                enabled = currentYear < maxYear
            ) {
                Icon(
                    imageVector = Icons.Filled.KeyboardArrowRight,
                    contentDescription = "增加年份"
                )
            }
        }
        
        Spacer(modifier = Modifier.height(8.dp))
        
        // 年份滑块
        Slider(
            value = sliderValue,
            onValueChange = { newValue ->
                sliderValue = newValue
                // 根据滑块值计算年份
                val newYear = (minYear + (maxYear - minYear) * newValue).roundToInt()
                if (newYear != currentYear) {
                    currentYear = newYear
                    onYearChanged(currentYear)
                }
            },
            colors = SliderDefaults.colors(
                thumbColor = MaterialTheme.colorScheme.primary,
                activeTrackColor = MaterialTheme.colorScheme.primary,
                inactiveTrackColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.3f)
            ),
            modifier = Modifier.fillMaxWidth()
        )
        
        // 年份范围标签
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = minYear.toString(),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
            )
            Text(
                text = maxYear.toString(),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
            )
        }
    }
}

/**
 * 年份范围选择器组件
 * 用于选择要查看的年份范围
 */
@Composable
fun YearRangeSelector(
    initialStartYear: Int,
    initialEndYear: Int,
    minYear: Int,
    maxYear: Int,
    onYearRangeChanged: (Int, Int) -> Unit
) {
    // 计算初始滑块值
    val yearRange = maxYear - minYear
    val initialStartValue = (initialStartYear - minYear).toFloat() / yearRange.toFloat()
    val initialEndValue = (initialEndYear - minYear).toFloat() / yearRange.toFloat()
    
    // 创建状态
    var startValue by remember { mutableFloatStateOf(initialStartValue) }
    var endValue by remember { mutableFloatStateOf(initialEndValue) }
    var startYear by remember { mutableStateOf(initialStartYear) }
    var endYear by remember { mutableStateOf(initialEndYear) }
    
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
    ) {
        // 年份范围标题
        Text(
            text = stringResource(id = R.string.trends_year_range),
            style = MaterialTheme.typography.bodyLarge,
            modifier = Modifier.padding(bottom = 16.dp)
        )
        
        // 年份范围显示
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = startYear.toString(),
                style = MaterialTheme.typography.titleMedium
            )
            Text(
                text = "-",
                style = MaterialTheme.typography.titleMedium
            )
            Text(
                text = endYear.toString(),
                style = MaterialTheme.typography.titleMedium
            )
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // 开始年份滑块
        Column {
            Text(
                text = "开始年份",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
            )
            Slider(
                value = startValue,
                onValueChange = { newValue ->
                    // 确保开始年份不大于结束年份
                    val tentativeNewValue = newValue.coerceAtMost(endValue - 0.05f)
                    if (tentativeNewValue != startValue) {
                        startValue = tentativeNewValue
                        // 根据滑块值计算年份
                        val newStartYear = (minYear + yearRange * startValue).roundToInt()
                        if (newStartYear != startYear) {
                            startYear = newStartYear
                            onYearRangeChanged(startYear, endYear)
                        }
                    }
                },
                colors = SliderDefaults.colors(
                    thumbColor = MaterialTheme.colorScheme.primary,
                    activeTrackColor = MaterialTheme.colorScheme.primary,
                    inactiveTrackColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.3f)
                ),
                modifier = Modifier.fillMaxWidth()
            )
        }
        
        Spacer(modifier = Modifier.height(8.dp))
        
        // 结束年份滑块
        Column {
            Text(
                text = "结束年份",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
            )
            Slider(
                value = endValue,
                onValueChange = { newValue ->
                    // 确保结束年份不小于开始年份
                    val tentativeNewValue = newValue.coerceAtLeast(startValue + 0.05f)
                    if (tentativeNewValue != endValue) {
                        endValue = tentativeNewValue
                        // 根据滑块值计算年份
                        val newEndYear = (minYear + yearRange * endValue).roundToInt()
                        if (newEndYear != endYear) {
                            endYear = newEndYear
                            onYearRangeChanged(startYear, endYear)
                        }
                    }
                },
                colors = SliderDefaults.colors(
                    thumbColor = MaterialTheme.colorScheme.primary,
                    activeTrackColor = MaterialTheme.colorScheme.primary,
                    inactiveTrackColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.3f)
                ),
                modifier = Modifier.fillMaxWidth()
            )
        }
        
        // 年份范围标签
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = minYear.toString(),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
            )
            Text(
                text = maxYear.toString(),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
            )
        }
    }
} 