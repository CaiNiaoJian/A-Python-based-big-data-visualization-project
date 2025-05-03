import axios from 'axios'
import * as XLSX from 'xlsx'

// 缓存数据
let cachedMilitaryData = null
let cachedCountries = null

/**
 * 从Excel文件加载军事数据
 */
export async function loadMilitaryData() {
  if (cachedMilitaryData) {
    return cachedMilitaryData
  }

  try {
    const result = []
    const continents = ['african', 'american', 'aisan', 'europen', 'easternasian']
    
    for (const continent of continents) {
      const response = await axios.get(`/rbdata/${continent}.xlsx`, { responseType: 'arraybuffer' })
      const workbook = XLSX.read(new Uint8Array(response.data), { type: 'array' })
      const sheet = workbook.Sheets[workbook.SheetNames[0]]
      const data = XLSX.utils.sheet_to_json(sheet, { header: 1 })
      
      // 第一行是表头
      const headers = data[0]
      const years = headers.slice(1).map((_, index) => 1960 + index)
      
      // 处理数据行
      for (let i = 1; i < data.length; i++) {
        const row = data[i]
        if (!row || !row[0]) continue
        
        const countryName = row[0]
        
        // 处理每一列（年份）的数据
        for (let j = 1; j < row.length; j++) {
          if (row[j] !== undefined && row[j] !== null && row[j] !== '...' && row[j] !== 'xx') {
            const year = years[j - 1]
            const expenditure = parseFloat(row[j])
            
            if (!isNaN(expenditure)) {
              result.push({
                country: countryName,
                year,
                expenditure,
                continent: getContinentFromFileName(continent)
              })
            }
          }
        }
      }
    }
    
    cachedMilitaryData = result
    return result
  } catch (error) {
    console.error('加载军事数据失败:', error)
    return []
  }
}

/**
 * 从Excel文件加载国家信息
 */
export async function loadCountries() {
  if (cachedCountries) {
    return cachedCountries
  }

  try {
    const result = []
    const continents = ['african', 'american', 'aisan', 'europen', 'easternasian']
    
    for (const continent of continents) {
      const response = await axios.get(`/rbdata/${continent}.xlsx`, { responseType: 'arraybuffer' })
      const workbook = XLSX.read(new Uint8Array(response.data), { type: 'array' })
      const sheet = workbook.Sheets[workbook.SheetNames[0]]
      const data = XLSX.utils.sheet_to_json(sheet, { header: 1 })
      
      // 处理数据行
      for (let i = 1; i < data.length; i++) {
        const row = data[i]
        if (!row || !row[0]) continue
        
        const countryName = row[0]
        
        // 检查是否已经添加过该国家
        if (!result.find(c => c.name === countryName)) {
          result.push({
            name: countryName,
            continent: getContinentFromFileName(continent),
            isoCode: '' // 暂时留空
          })
        }
      }
    }
    
    cachedCountries = result
    return result
  } catch (error) {
    console.error('加载国家信息失败:', error)
    return []
  }
}

/**
 * 根据文件名获取大洲名称
 */
function getContinentFromFileName(fileName) {
  const continentMap = {
    'african': '非洲',
    'american': '美洲',
    'aisan': '亚洲',
    'europen': '欧洲',
    'easternasian': '东亚'
  }
  
  return continentMap[fileName] || '未知'
}

/**
 * 获取特定年份的数据
 */
export async function getDataByYear(year) {
  const data = await loadMilitaryData()
  return data.filter(item => item.year === year)
}

/**
 * 获取特定国家的数据
 */
export async function getDataByCountry(countryName) {
  const data = await loadMilitaryData()
  return data.filter(item => item.country === countryName)
}

/**
 * 获取特定年份和大洲的数据
 */
export async function getDataByYearAndContinent(year, continent) {
  const data = await loadMilitaryData()
  return data.filter(item => item.year === year && item.continent === continent)
}

/**
 * 获取排名前N的国家数据
 */
export async function getTopCountriesByYear(year, limit = 20) {
  const yearData = await getDataByYear(year)
  const sortedData = yearData
    .sort((a, b) => b.expenditure - a.expenditure)
    .slice(0, limit)
  
  // 添加排名
  sortedData.forEach((item, index) => {
    item.rank = index + 1
  })
  
  return sortedData
}

/**
 * 获取国家的年度趋势数据
 */
export async function getCountryTrend(countryName, startYear, endYear) {
  const countryData = await getDataByCountry(countryName)
  return countryData
    .filter(item => item.year >= startYear && item.year <= endYear)
    .sort((a, b) => a.year - b.year)
}

/**
 * 获取两个国家的比较数据
 */
export async function compareCountries(country1, country2, startYear, endYear) {
  const [data1, data2] = await Promise.all([
    getCountryTrend(country1, startYear, endYear),
    getCountryTrend(country2, startYear, endYear)
  ])
  
  return {
    country1: { name: country1, data: data1 },
    country2: { name: country2, data: data2 }
  }
}

/**
 * 获取特定年份各大洲的军费总和
 */
export async function getContinentTotalsByYear(year) {
  const yearData = await getDataByYear(year)
  const continentTotals = {}
  
  // 定义所有大洲列表，确保结果中包含所有大洲
  const allContinents = ['非洲', '美洲', '亚洲', '欧洲', '东亚']
  allContinents.forEach(continent => {
    continentTotals[continent] = 0
  })
  
  // 计算每个大洲的总和
  yearData.forEach(item => {
    if (item.continent && continentTotals[item.continent] !== undefined) {
      continentTotals[item.continent] += item.expenditure
    }
  })
  
  // 转换为数组格式返回
  return Object.keys(continentTotals).map(continent => ({
    continent,
    expenditure: continentTotals[continent]
  }))
}

/**
 * 获取全球军费总和的年度趋势
 */
export async function getGlobalTrend(startYear, endYear) {
  const allData = await loadMilitaryData()
  const yearTotals = {}
  
  // 初始化所有年份的数据为0
  for (let year = startYear; year <= endYear; year++) {
    yearTotals[year] = 0
  }
  
  // 计算每年的总和
  allData.forEach(item => {
    if (item.year >= startYear && item.year <= endYear) {
      yearTotals[item.year] += item.expenditure
    }
  })
  
  // 转换为数组格式返回
  return Object.keys(yearTotals)
    .map(year => ({
      year: parseInt(year),
      expenditure: yearTotals[year]
    }))
    .sort((a, b) => a.year - b.year)
}

/**
 * 获取大洲军费总和的年度趋势
 */
export async function getContinentTrend(continent, startYear, endYear) {
  const allData = await loadMilitaryData()
  const yearTotals = {}
  
  // 初始化所有年份的数据为0
  for (let year = startYear; year <= endYear; year++) {
    yearTotals[year] = 0
  }
  
  // 计算每年的总和
  allData.forEach(item => {
    if (item.continent === continent && item.year >= startYear && item.year <= endYear) {
      yearTotals[item.year] += item.expenditure
    }
  })
  
  // 转换为数组格式返回
  return Object.keys(yearTotals)
    .map(year => ({
      year: parseInt(year),
      expenditure: yearTotals[year]
    }))
    .sort((a, b) => a.year - b.year)
}

/**
 * 获取所有可用的年份列表
 */
export async function getAllYears() {
  const data = await loadMilitaryData()
  const yearSet = new Set()
  
  data.forEach(item => {
    yearSet.add(item.year)
  })
  
  return Array.from(yearSet).sort()
}

/**
 * 清除数据缓存
 */
export function clearCache() {
  cachedMilitaryData = null
  cachedCountries = null
  console.log('数据缓存已清除')
} 