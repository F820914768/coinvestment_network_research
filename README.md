# coinvestment_network_research

This is to study the co-investment networks of assets. 

## Introduction

Security market can make someone a millionaire in one day, as well as make someone bankrupt. Normally, high quality security can have high return, and high risk. To determine one’s holding on securities, return, risk and quality of a security.

The idea here is simple: 
the asset which is hold by the majority of investor is likely to be quality asset and have high return and high risk; If two assets are hold by the same group of investors, the two assets are likely to be similar, and their return and price are likely to be correlated.

Mutual funds are best candidate to study network structure, since the holding of mutual funds is open, and mutual funds form a large portion of security market. 


## Networks model

There are two networks in our model:

The first network is stock co-investment network, where node represents stock, edge represents common investment. If two stocks u and v are both invested by N numbers of mutual funds, the weight of edge between u and v will be N.

The second network is fund network. Similar to stock network, here nodes represent mutual funds where edge with weight N represents the two funds have N numbers of common holdings.


## Our work

* We write a crawler to fetch stocks data and mutual funds data from yahoo.
* ...

## How to use

<table>
  <tr>
       <th>Script Name</th><th>API</th>
  </tr>
        <td>create_db.py</td><td>run "python create_db.py [csv/xslx]" to convert a csv or xslx file into database table 
        <br></br> E.X. "python create_db.py funds_holding.csv"</td>
  <tr>
        <td>query.py</td><td>Edit String variable <i>query</i> in query.py. Then run script, the result query will be saved into a csv file</td>
  </tr>
  <tr>
  </tr>
</table>
