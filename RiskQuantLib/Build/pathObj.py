#!/usr/bin/python
#coding = utf-8
import os

class pathObj():
    """
    pathObj() is a registration class, which stores the file path and class information.
    The information stored here will be used to locate files across the whole project.

    This class itself can also be built. It will be auto-updated once a new instrument are specified and committed.
    """
    pathDict = {}
    pathDict['Any'] = 'Set' + os.sep + 'Security' + os.sep + 'base.py'
    pathDict['Stock'] = 'Set' + os.sep + 'Security' + os.sep + 'Stock' + os.sep + 'stock.py'
    pathDict[
        'Index Underlying Stock'] = 'Set' + os.sep + 'Security' + os.sep + 'Stock' + os.sep + 'stockIndexUnderlyingStock.py'
    pathDict['Fund'] = 'Set' + os.sep + 'Security' + os.sep + 'Fund' + os.sep + 'fund.py'
    pathDict['Bond'] = 'Set' + os.sep + 'Security' + os.sep + 'Bond' + os.sep + 'bond.py'
    pathDict[
        'Index Underlying Bond'] = 'Set' + os.sep + 'Security' + os.sep + 'Bond' + os.sep + 'bondIndexUnderlyingBond.py'
    pathDict['Derivative'] = 'Set' + os.sep + 'Security' + os.sep + 'Derivative' + os.sep + 'derivative.py'
    pathDict['Option'] = 'Set' + os.sep + 'Security' + os.sep + 'Derivative' + os.sep + 'Option' + os.sep + 'option.py'
    pathDict['Future'] = 'Set' + os.sep + 'Security' + os.sep + 'Derivative' + os.sep + 'Future' + os.sep + 'future.py'
    pathDict['Index Future'] = 'Set' + os.sep + 'Security' + os.sep + 'Derivative' + os.sep + 'Future' + os.sep + 'indexFuture.py'
    pathDict['Bond Future'] = 'Set' + os.sep + 'Security' + os.sep + 'Derivative' + os.sep + 'Future' + os.sep + 'bondFuture.py'
    pathDict['Repo'] = 'Set' + os.sep + 'Security' + os.sep + 'Repo' + os.sep + 'repo.py'
    pathDict['Convertible Bond'] = 'Set' + os.sep + 'Security' + os.sep + 'Bond' + os.sep + 'convertibleBond.py'
    pathDict['Interest Rate'] = 'Set' + os.sep + 'InterestRate' + os.sep + 'base.py'
    pathDict['Index'] = 'Set' + os.sep + 'Index' + os.sep + 'base.py'
    pathDict['Bond Index'] = 'Set' + os.sep + 'Index' + os.sep + 'BondIndex' + os.sep + 'bondIndex.py'
    pathDict['Stock Index'] = 'Set' + os.sep + 'Index' + os.sep + 'StockIndex' + os.sep + 'stockIndex.py'
    pathDict['Company'] = 'Set' + os.sep + 'Company' + os.sep + 'base.py'
    pathDict['Listed Company'] = 'Set' + os.sep + 'Company' + os.sep + 'ListedCompany' + os.sep + 'listedCompany.py'
    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<pathDictBegin>
    #-<pathDictEnd>

    listPathDict = {}
    listPathDict['Any'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'base.py'
    listPathDict['Stock'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'StockList' + os.sep + 'stockList.py'
    listPathDict[
        'Index Underlying Stock'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'StockList' + os.sep + 'stockIndexUnderlyingStockList.py'
    listPathDict['Fund'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'FundList' + os.sep + 'fundList.py'
    listPathDict['Bond'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'BondList' + os.sep + 'bondList.py'
    listPathDict[
        'Index Underlying Bond'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'BondList' + os.sep + 'bondIndexUnderlyingBondList.py'
    listPathDict['Derivative'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'DerivativeList' + os.sep + 'derivativeList.py'
    listPathDict['Option'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'DerivativeList' + os.sep + 'OptionList' + os.sep + 'optionList.py'
    listPathDict['Future'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'DerivativeList' + os.sep + 'FutureList' + os.sep + 'futureList.py'
    listPathDict['Index Future'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'DerivativeList' + os.sep + 'FutureList' + os.sep + 'indexFutureList.py'
    listPathDict['Bond Future'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'DerivativeList' + os.sep + 'FutureList' + os.sep + 'bondFutureList.py'
    listPathDict['Repo'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'RepoList' + os.sep + 'repoList.py'
    listPathDict['Convertible Bond'] = 'Set' + os.sep + 'SecurityList' + os.sep + 'BondList' + os.sep + 'convertibleBondList.py'
    listPathDict['Index'] = 'Set' + os.sep + 'IndexList' + os.sep + 'base.py'
    listPathDict['Bond Index'] = 'Set' + os.sep + 'IndexList' + os.sep + 'BondIndexList' + os.sep + 'bondIndexList.py'
    listPathDict[
        'Stock Index'] = 'Set' + os.sep + 'IndexList' + os.sep + 'StockIndexList' + os.sep + 'stockIndexList.py'
    listPathDict['Company'] = 'Set' + os.sep + 'CompanyList' + os.sep + 'base.py'
    listPathDict[
        'Listed Company'] = 'Set' + os.sep + 'CompanyList' + os.sep + 'ListedCompanyList' + os.sep + 'listedCompanyList.py'
    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<listPathDictBegin>
    #-<listPathDictEnd>
    
    classPathDict = {}
    classPathDict['Any'] = 'RiskQuantLib.Security.base'
    classPathDict['Stock'] = 'RiskQuantLib.Security.Stock.stock'
    classPathDict['Index Underlying Stock'] = 'RiskQuantLib.Security.Stock.stockIndexUnderlyingStock'
    classPathDict['Fund'] = 'RiskQuantLib.Security.Fund.fund'
    classPathDict['Bond'] = 'RiskQuantLib.Security.Bond.bond'
    classPathDict['Index Underlying Bond'] = 'RiskQuantLib.Security.Bond.bondIndexUnderlyingBond'
    classPathDict['Derivative'] = 'RiskQuantLib.Security.Derivative.derivative'
    classPathDict['Option'] = 'RiskQuantLib.Security.Derivative.Option.option'
    classPathDict['Future'] = 'RiskQuantLib.Security.Derivative.Future.future'
    classPathDict['Index Future'] = 'RiskQuantLib.Security.Derivative.Future.indexFuture'
    classPathDict['Bond Future'] = 'RiskQuantLib.Security.Derivative.Future.bondFuture'
    classPathDict['Repo'] = 'RiskQuantLib.Security.Repo.repo'
    classPathDict['Convertible Bond'] = 'RiskQuantLib.Security.Bond.convertibleBond'
    classPathDict['Interest Rate'] = 'RiskQuantLib.InterestRate.base'
    classPathDict['Index'] = 'RiskQuantLib.Index.base'
    classPathDict['Bond Index'] = 'RiskQuantLib.Index.BondIndex.bondIndex'
    classPathDict['Stock Index'] = 'RiskQuantLib.Index.StockIndex.stockIndex'
    classPathDict['Company'] = 'RiskQuantLib.Company.base'
    classPathDict['Listed Company'] = 'RiskQuantLib.Company.ListedCompany.listedCompany'
    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<classPathDictBegin>
    #-<classPathDictEnd>

    classNameDict = {}
    classNameDict['Any'] = 'base'
    classNameDict['Stock'] = 'stock'
    classNameDict['Index Underlying Stock'] = 'stockIndexUnderlyingStock'
    classNameDict['Fund'] = 'fund'
    classNameDict['Bond'] = 'bond'
    classNameDict['Index Underlying Bond'] = 'bondIndexUnderlyingBond'
    classNameDict['Derivative'] = 'derivative'
    classNameDict['Option'] = 'option'
    classNameDict['Future'] = 'future'
    classNameDict['Index Future'] = 'indexFuture'
    classNameDict['Bond Future'] = 'bondFuture'
    classNameDict['Repo'] = 'repo'
    classNameDict['Convertible Bond'] = 'convertibleBond'
    classNameDict['Interest Rate'] = 'base'
    classNameDict['Index'] = 'base'
    classNameDict['Bond Index'] = 'bondIndex'
    classNameDict['Stock Index'] = 'stockIndex'
    classNameDict['Company'] = 'base'
    classNameDict['Listed Company'] = 'listedCompany'
    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<classNameDictBegin>
    #-<classNameDictEnd>

    attributeTypeDefaultList = ['Any', 'Average', 'Amount', 'Aum', 'Beta', 'Cost', 'Duration', 'Dv01', 'FaceValue',
                         'InterestRate', 'MarketValue', 'Nav', 'Number', 'Price', 'ProfitAndLoss', 'Weight', 'Series',
                         'String']
    attributeTypeDict = {}
    attributeTypeDict['Any'] = 'Property' + os.sep + 'base.py'
    attributeTypeDict['Average'] = 'Property' + os.sep + 'average.py'
    attributeTypeDict['Amount'] = 'Property' + os.sep + 'Amount' + os.sep + 'amount.py'
    attributeTypeDict['Aum'] = 'Property' + os.sep + 'Aum' + os.sep + 'aum.py'
    attributeTypeDict['Beta'] = 'Property' + os.sep + 'Beta' + os.sep + 'beta.py'
    attributeTypeDict['Cost'] = 'Property' + os.sep + 'Cost' + os.sep + 'cost.py'
    attributeTypeDict['Duration'] = 'Property' + os.sep + 'Duration' + os.sep + 'duration.py'
    attributeTypeDict['Dv01'] = 'Property' + os.sep + 'Dv01' + os.sep + 'dv01.py'
    attributeTypeDict['FaceValue'] = 'Property' + os.sep + 'FaceValue' + os.sep + 'faceValue.py'
    attributeTypeDict['InterestRate'] = 'Property' + os.sep + 'InterestRate' + os.sep + 'interestRate.py'
    attributeTypeDict['MarketValue'] = 'Property' + os.sep + 'MarketValue' + os.sep + 'marketValue.py'
    attributeTypeDict['Nav'] = 'Property' + os.sep + 'Nav' + os.sep + 'nav.py'
    attributeTypeDict['Number'] = 'Property' + os.sep + 'NumberProperty' + os.sep + 'numberProperty.py'
    attributeTypeDict['Price'] = 'Property' + os.sep + 'Price' + os.sep + 'price.py'
    attributeTypeDict['ProfitAndLoss'] = 'Property' + os.sep + 'ProfitAndLoss' + os.sep + 'profitAndLoss.py'
    attributeTypeDict['Weight'] = 'Property' + os.sep + 'Weight' + os.sep + 'weight.py'
    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<attributeTypeDictBegin>
    #-<attributeTypeDictEnd>

    def __init__(self):
        pass