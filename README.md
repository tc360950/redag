# About 
REDAG (Relational Data Generator) is a small python framework for generation of random data from relation model. 

For instance, consider a simplified model of Accounts Receivable data. 

A producer has a fixed portfolio of *Items*. Customer transaction request results in creation of a *SalesOrder* which corresponds to 
some quantity of an item from the portfolio. In the process of transaction some number of *Invoices* (which correspond to the sales order) is issued to the customer. 
Eventually ordered items are issued from the warehouse through *WarehouseOrder*. 

*Item*, *SalesOrder*, *Invoice*, *WarehouseOrder* are what we call entities. 
They are connected through directed acyclic relation graph:
```mermaid
  graph TD;
      A-->B;
      A-->C;
      B-->D;
      C-->D;
```


# Usage