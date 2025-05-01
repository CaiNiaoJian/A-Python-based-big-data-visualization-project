package com.military.visualization.data.loader

import android.content.Context
import android.util.Log
import com.military.visualization.data.model.Country
import com.military.visualization.data.model.MilitaryData
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.apache.poi.ss.usermodel.CellType
import org.apache.poi.ss.usermodel.WorkbookFactory
import java.io.InputStream
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Excel数据加载器
 * 用于从Excel文件加载军事数据
 */
@Singleton
class ExcelDataLoader @Inject constructor(
    private val context: Context
) {
    companion object {
        private const val TAG = "ExcelDataLoader"
        
        // 资源文件中的Excel文件名
        private val EXCEL_FILES = listOf(
            "african.xlsx",
            "american.xlsx",
            "aisan.xlsx",
            "europen.xlsx",
            "easternasian.xlsx"
        )
        
        // 大洲名称映射
        private val CONTINENT_MAP = mapOf(
            "african.xlsx" to "非洲",
            "american.xlsx" to "美洲",
            "aisan.xlsx" to "亚洲",
            "europen.xlsx" to "欧洲",
            "easternasian.xlsx" to "东亚"
        )
    }
    
    /**
     * 从资源文件加载所有军事数据
     */
    suspend fun loadAllMilitaryData(): List<MilitaryData> = withContext(Dispatchers.IO) {
        val result = mutableListOf<MilitaryData>()
        
        try {
            // 加载所有Excel文件
            for (fileName in EXCEL_FILES) {
                val inputStream = openExcelFile(fileName)
                if (inputStream != null) {
                    result.addAll(parseMilitaryDataFromExcel(inputStream, fileName))
                }
            }
        } catch (e: Exception) {
            Log.e(TAG, "加载军事数据失败: ${e.message}", e)
        }
        
        return@withContext result
    }
    
    /**
     * 加载所有国家信息
     */
    suspend fun loadAllCountries(): List<Country> = withContext(Dispatchers.IO) {
        val result = mutableListOf<Country>()
        
        try {
            // 加载所有Excel文件
            for (fileName in EXCEL_FILES) {
                val inputStream = openExcelFile(fileName)
                if (inputStream != null) {
                    result.addAll(parseCountriesFromExcel(inputStream, fileName))
                }
            }
        } catch (e: Exception) {
            Log.e(TAG, "加载国家信息失败: ${e.message}", e)
        }
        
        return@withContext result
    }
    
    /**
     * 打开Excel文件
     */
    private fun openExcelFile(fileName: String): InputStream? {
        return try {
            context.assets.open("rbdata/$fileName")
        } catch (e: Exception) {
            Log.e(TAG, "打开Excel文件失败: $fileName, ${e.message}", e)
            null
        }
    }
    
    /**
     * 从Excel文件解析军事数据
     */
    private fun parseMilitaryDataFromExcel(inputStream: InputStream, fileName: String): List<MilitaryData> {
        val result = mutableListOf<MilitaryData>()
        
        try {
            val workbook = WorkbookFactory.create(inputStream)
            val sheet = workbook.getSheetAt(0)
            
            // 默认年份范围（1960-2022）
            val defaultYears = (1960..2022).toList()
            
            // 读取每一行数据（第一列是国家名称，后面的列是各年份的军费开支）
            for (rowIndex in 0 until sheet.physicalNumberOfRows) {
                val row = sheet.getRow(rowIndex) ?: continue
                
                // 读取国家名称
                val countryCell = row.getCell(0)
                val countryName = when (countryCell?.cellType) {
                    CellType.STRING -> countryCell.stringCellValue
                    CellType.NUMERIC -> countryCell.numericCellValue.toString()
                    else -> continue
                }
                
                // 读取各年份的军费开支
                for (colIndex in 1 until row.physicalNumberOfCells) {
                    // 确保年份索引不超出范围
                    val yearIndex = colIndex - 1
                    if (yearIndex >= defaultYears.size) continue
                    
                    val year = defaultYears[yearIndex]
                    val cell = row.getCell(colIndex)
                    
                    // 跳过空单元格和非数值单元格
                    if (cell == null) continue
                    if (cell.cellType != CellType.NUMERIC && cell.cellType != CellType.STRING) continue
                    
                    // 读取军费开支
                    val expenditure = when (cell.cellType) {
                        CellType.NUMERIC -> cell.numericCellValue
                        CellType.STRING -> {
                            val value = cell.stringCellValue
                            if (value == "..." || value == "xx") {
                                // 缺失值或未记录，跳过
                                continue
                            } else {
                                try {
                                    value.toDouble()
                                } catch (e: Exception) {
                                    // 无法解析为数值，跳过
                                    continue
                                }
                            }
                        }
                        else -> continue
                    }
                    
                    // 创建军事数据对象
                    val militaryData = MilitaryData(
                        country = countryName,
                        year = year,
                        expenditure = expenditure
                    )
                    
                    result.add(militaryData)
                }
            }
            
            workbook.close()
        } catch (e: Exception) {
            Log.e(TAG, "解析Excel文件失败: $fileName, ${e.message}", e)
        }
        
        return result
    }
    
    /**
     * 从Excel文件解析国家信息
     */
    private fun parseCountriesFromExcel(inputStream: InputStream, fileName: String): List<Country> {
        val result = mutableListOf<Country>()
        val continent = CONTINENT_MAP[fileName] ?: "未知"
        
        try {
            val workbook = WorkbookFactory.create(inputStream)
            val sheet = workbook.getSheetAt(0)
            
            // 读取每一行数据（第一列是国家名称）
            for (rowIndex in 0 until sheet.physicalNumberOfRows) {
                val row = sheet.getRow(rowIndex) ?: continue
                
                // 读取国家名称
                val countryCell = row.getCell(0)
                val countryName = when (countryCell?.cellType) {
                    CellType.STRING -> countryCell.stringCellValue
                    CellType.NUMERIC -> countryCell.numericCellValue.toString()
                    else -> continue
                }
                
                // 创建国家信息对象（ISO代码暂时留空，后续可以通过其他方式补充）
                val country = Country(
                    name = countryName,
                    continent = continent,
                    isoCode = ""  // 暂时留空
                )
                
                result.add(country)
            }
            
            workbook.close()
        } catch (e: Exception) {
            Log.e(TAG, "解析Excel文件失败: $fileName, ${e.message}", e)
        }
        
        return result
    }
} 