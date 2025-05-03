import axios from 'axios'

// 缓存数据
let cachedYearsSummary = null
let cachedCountryMetadata = null
let cachedYearsData = {}
let cachedContinentData = {}

/**
 * 获取年度摘要信息
 */
export async function getYearsSummary() {
  if (cachedYearsSummary) {
    return cachedYearsSummary
  }
  
  try {
    const response = await axios.get('/rbdata/data/years_summary.json')
    cachedYearsSummary = response.data
    return cachedYearsSummary
  } catch (error) {
    console.error('加载年度摘要数据失败:', error)
    return {}
  }
}

/**
 * 获取国家元数据
 */
export async function getCountryMetadata() {
  if (cachedCountryMetadata) {
    return cachedCountryMetadata
  }
  
  try {
    const response = await axios.get('/rbdata/data/country_metadata.json')
    cachedCountryMetadata = response.data
    return cachedCountryMetadata
  } catch (error) {
    console.error('加载国家元数据失败:', error)
    return {}
  }
}

/**
 * 获取特定年份的数据
 */
export async function getYearData(year) {
  if (cachedYearsData[year]) {
    return cachedYearsData[year]
  }
  
  try {
    const response = await axios.get(`/rbdata/data/year_${year}.json`)
    cachedYearsData[year] = response.data
    return response.data
  } catch (error) {
    console.error(`加载${year}年数据失败:`, error)
    return []
  }
}

/**
 * 获取特定大洲的数据
 */
export async function getContinentData(continent) {
  if (cachedContinentData[continent]) {
    return cachedContinentData[continent]
  }
  
  try {
    const response = await axios.get(`/rbdata/data/${continent}.json`)
    cachedContinentData[continent] = response.data
    return response.data
  } catch (error) {
    console.error(`加载${continent}大洲数据失败:`, error)
    return []
  }
}

/**
 * 获取所有年份的列表
 */
export async function getAllYears() {
  const summary = await getYearsSummary()
  return Object.keys(summary).map(year => parseInt(year)).sort()
}

/**
 * 获取国家列表
 */
export async function getCountryList() {
  const metadata = await getCountryMetadata()
  // 获取所有国家名称
  const allCountries = Object.keys(metadata)
  
  // 确保美国和中国排在最前面
  return allCountries.sort((a, b) => {
    // 让美国排第一位
    if (a === '美国') return -1
    if (b === '美国') return 1
    // 让中国排第二位
    if (a === '中国') return -1
    if (b === '中国') return 1
    // 其他国家按字母排序
    return a.localeCompare(b, 'zh-CN')
  })
}

/**
 * 根据年份获取排名前N的国家
 */
export async function getTopCountriesByYear(year, limit = 20) {
  const yearData = await getYearData(year)
  
  return yearData
    .sort((a, b) => b.Expenditure - a.Expenditure)
    .slice(0, limit)
    .map((item, index) => ({
      country: item.Country,
      expenditure: item.Expenditure,
      continent: item.Continent,
      rank: index + 1
    }))
}

/**
 * 根据国家获取历年数据
 */
export async function getCountryHistoricalData(country) {
  const years = await getAllYears()
  const result = []
  
  for (const year of years) {
    const yearData = await getYearData(year)
    const countryData = yearData.find(item => item.Country === country)
    
    if (countryData) {
      result.push({
        year,
        expenditure: countryData.Expenditure
      })
    }
  }
  
  return result.sort((a, b) => a.year - b.year)
}

/**
 * 比较两个国家在特定年份范围内的数据
 */
export async function compareCountries(country1, country2, startYear, endYear) {
  const data1 = await getCountryHistoricalData(country1)
  const data2 = await getCountryHistoricalData(country2)
  
  return {
    country1: {
      name: country1,
      data: data1.filter(item => item.year >= startYear && item.year <= endYear)
    },
    country2: {
      name: country2,
      data: data2.filter(item => item.year >= startYear && item.year <= endYear)
    },
    years: Array.from({ length: endYear - startYear + 1 }, (_, i) => startYear + i)
  }
}

/**
 * 获取特定年份两个国家的对比统计信息
 */
export async function getCountryComparisonStats(country1, country2, year) {
  const yearData = await getYearData(year)
  const allCountries = yearData.sort((a, b) => b.Expenditure - a.Expenditure)
  
  const country1Data = allCountries.find(item => item.Country === country1)
  const country2Data = allCountries.find(item => item.Country === country2)
  
  if (!country1Data || !country2Data) {
    return null
  }
  
  const country1Rank = allCountries.findIndex(item => item.Country === country1) + 1
  const country2Rank = allCountries.findIndex(item => item.Country === country2) + 1
  
  return {
    year,
    country1: {
      name: country1,
      expenditure: country1Data.Expenditure,
      rank: country1Rank,
      continent: country1Data.Continent
    },
    country2: {
      name: country2,
      expenditure: country2Data.Expenditure,
      rank: country2Rank,
      continent: country2Data.Continent
    },
    difference: Math.abs(country1Data.Expenditure - country2Data.Expenditure),
    ratio: Math.max(country1Data.Expenditure, country2Data.Expenditure) / 
           Math.min(country1Data.Expenditure, country2Data.Expenditure)
  }
}

/**
 * 获取不同大洲在特定年份的军费开支总和
 */
export async function getContinentExpenditureByYear(year) {
  const yearData = await getYearData(year)
  
  const continentTotals = {}
  
  yearData.forEach(item => {
    if (!continentTotals[item.Continent]) {
      continentTotals[item.Continent] = 0
    }
    continentTotals[item.Continent] += item.Expenditure
  })
  
  return Object.keys(continentTotals).map(continent => ({
    continent,
    expenditure: continentTotals[continent]
  }))
}

/**
 * 清除缓存
 */
export function clearCache() {
  cachedYearsSummary = null
  cachedCountryMetadata = null
  cachedYearsData = {}
  cachedContinentData = {}
} 