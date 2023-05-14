#!/usr/bin/env python
# coding: utf-8

# # Capstone Project Flask UI

# Pada capstone ini anda diminta untuk membangun sebuah Flask UI sederhana yang berisi beberapa tampilan plot dari skeleton yang sudah disediakan dan satu plot tambahan berdasarkan analisis anda.
# 
# File ini dapat dimanfaatkan untuk membantu anda dalam proses wrangling dan visualization. Apabila proses wrangling sudah tepat dan hasil visualisasi sudah sesuai dengan ketentuan, anda dapat memindahkan kembali kode program yang sudah anda lengkapi ke dalam file `app.py`.

# ## Data Preprocessing

# **Import library**

# In[81]:


# !pip install Flask
from flask import Flask, render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64


# **Load data**
# 
# Bacalah file `googleplaystore.csv` data dan simpan ke objek dataframe dengan nama playstore

# In[82]:


playstore = pd.read_csv('data/googleplaystore.csv')
playstore


# **Data Cleansing** 

# **_Task 1:_** Hapus data yang duplikat berdasarkan kolom App, dengan tetap keep data pertama (hint : gunakan parameter subset)

# In[83]:


playstore['Category'].unique()


# In[84]:


cektabelcategory=playstore['Category'].value_counts(ascending=False)
cektabelcategory


# In[85]:


playstore=playstore.drop_duplicates(subset ='App', keep = 'first')
#playstore._________(subset = ___________________) 
playstore


# In[86]:


cektabelcategory


# Bagian ini untuk menghapus row 10472 karena nilai data tersebut tidak tersimpan pada kolom yang benar

# In[87]:


#playstore.iloc[10472]
playstore.drop([10472], inplace=True)


# In[88]:


playstore


# In[89]:


cektabelcategory=playstore['Category'].value_counts(ascending=False)
cektabelcategory


# **_Task 2:_** Cek tipe data kolom Category. Jika masih tersimpan dengan format tipe data yang salah, ubah ke tipe data yang sesuai
# 

# In[90]:


playstore.Category = playstore.Category.astype('category')


# In[91]:


playstore.dtypes


# **_Task 3:_** Pada kolom Installs Buang tanda koma(,) dan tanda tambah(+) kemudian ubah tipe data menjadi integer

# In[92]:


playstore['Category'].unique()


# In[93]:


playstore['Installs'].unique()


# In[94]:


playstore.Installs = playstore.Installs.apply(lambda x: x.replace('+',''))
playstore.Installs = playstore.Installs.apply(lambda x: x.replace(',',''))


# In[95]:


playstore['Installs'].unique()


# In[96]:


playstore.Installs = playstore.Installs.astype(int)
playstore.info()


# Bagian ini untuk merapikan kolom Size, Anda tidak perlu mengubah apapun di bagian ini

# In[97]:


playstore['Size'].replace('Varies with device', np.nan, inplace = True ) 
playstore.Size = (playstore.Size.replace(r'[kM]+$', '', regex=True).astype(float) *              playstore.Size.str.extract(r'[\d\.]+([kM]+)', expand=False)
            .fillna(1)
            .replace(['k','M'], [10**3, 10**6]).astype(int))
playstore['Size'].fillna(playstore.groupby('Category')['Size'].transform('mean'),inplace = True)


# **_Task 4:_** Pada kolom Price, buang karakater $ pada nilai Price lalu ubah tipe datanya menjadi float

# In[98]:


playstore['Price'].unique()


# In[99]:


playstore.Price = playstore.Price.apply(lambda x: x.replace('$',''))
playstore.Price = playstore.Price.astype(float)


# In[100]:


playstore['Price'].unique()


# In[101]:


playstore.info()


# Ubah tipe data Reviews, Size, Installs ke dalam tipe data integer

# In[102]:


##code here

playstore=playstore.astype({'Reviews':'int32','Size':'int32'})


# In[103]:


playstore.info()


# ## Data Wrangling

# In[104]:


df2 = playstore.copy()


# In[105]:


df2.head()


# **_Task 5:_** Dataframe top_category dibuat untuk menyimpan frekuensi aplikasi untuk setiap Category. 
# Gunakan crosstab untuk menghitung frekuensi aplikasi di setiap category kemudian gunakan `Jumlah`
# sebagai nama kolom dan urutkan nilai frekuensi dari nilai yang paling banyak. Terakhir reset index dari dataframe top_category.

# In[106]:


top_category=pd.crosstab(index=df2['Category'],
                            columns='Jumlah',).sort_values(by='Jumlah',ascending=False).reset_index()#.set_index('Category')
top_category.head()


# In[107]:


top_category.head()


# **_Task 6:_** Ini adalah bagian untuk melengkapi konten value box 
# most category mengambil nama category paling banyak mengacu pada dataframe `top_category`
# total mengambil frekuensi/jumlah category paling banyak mengacu pada dataframe `top_category`

# In[108]:


most_categories = top_category.iloc[0,0]
most_categories


# In[109]:


total = top_category.iloc[0,1]
total


# `rev_table` adalah tabel yang berisi 10 aplikasi yang paling banyak direview oleh pengguna.
# Silahkan melakukan agregasi data yang tepat menggunakan `groupby` untuk menampilkan 10 aplikasi yang diurutkan berdasarkan jumlah Review pengguna. 
# 
# Tabel yang ditampilkan terdiri dari 4 kolom yaitu nama Category, nama App, total Reviews, dan rata-rata Rating.
# Pindahkan kode wrangling yang disimpan dalam variable `rev_table` pada `blank code` yang telah di chaining dengan kode `.to_html`.

# In[110]:


rev_table=df2.groupby(['Category','App']).agg({'Reviews':'sum','Rating':'mean'}).sort_values(by='Reviews',ascending=False).reset_index()
rev_table.head(10)


# Apabila menuliskan kode program yang tepat maka hasil wrangling adalah sebagai berikut :

# In[111]:


#rev_table


# ## Data Visualization

# **Membuat Bar Plot**

# **_Task 7:_** 
# Lengkapi tahap agregasi untuk membuat dataframe yang mengelompokkan aplikasi berdasarkan Category.
# Buatlah bar plot dimana axis x adalah nama Category dan axis y adalah jumlah aplikasi pada setiap kategori, kemudian urutkan dari jumlah terbanyak

# In[112]:


#cat_order = df2.groupby(by='Category').agg({
#'App' : 'Count' }).rename({'Category':'Total'}, axis=1).sort_values(by='Total').head()
#X = _____________
#Y = _____________
#my_colors = 'rgbkymc'
# bagian ini digunakan untuk membuat kanvas/figure
#fig = plt.figure(figsize=(8,3),dpi=300)
#fig.add_subplot()
# bagian ini digunakan untuk membuat bar plot
#plt.barh(____,_____, color=my_colors)
# bagian ini digunakan untuk menyimpan plot dalam format image.png
#plt.savefig('cat_order.png',bbox_inches="tight") 


# In[113]:


cat_order = df2.groupby(by='Category').agg({
'Category' : 'count' }).rename({'Category':'Total'}, axis=1).sort_values(by='Total',ascending=False).head().reset_index()
X = cat_order['Category']
Y = cat_order['Total']
my_colors = ['r', 'g', 'b', 'k', 'y', 'm', 'c']
# bagian ini digunakan untuk membuat kanvas/figure
fig = plt.figure(figsize=(8,3),dpi=300)
fig.add_subplot()
# bagian ini digunakan untuk membuat bar plot
plt.barh(X ,Y ,color=my_colors)
# bagian ini digunakan untuk menyimpan plot dalam format image.png
plt.savefig('cat_order.png',bbox_inches="tight") 


# In[114]:


#rename app jadi total -
#cat_order = df2.groupby(by='Category').agg({
#'App' : 'count' }).rename({'App':'Total'}, axis=1).sort_values(by='Total',ascending=False).head().reset_index()
#cat_order


# **Membuat Scatter Plot**

# **_Task 8:_** Buatlah scatter plot untuk menampilkan hubungan dan persebaran apalikasi dilihat dari Review vs Rating.
# Ukuran scatter menggambarkan berapa banyak pengguna yang telah menginstall aplikasi 
#     

# In[115]:


#X = df2['______'].values # axis x
#Y = df2[______].values # axis y
#area = playstore[_______].values/10000000 # ukuran besar/kecilnya lingkaran scatter plot
#fig = plt.figure(figsize=(5,5))
#fig.add_subplot()
# isi nama method untuk scatter plot, variabel x, dan variabel y
#plt._______(x=_____,y=______, s=area, alpha=0.3)
#plt.xlabel('Reviews')
#plt.ylabel('Rating')
#plt.savefig('rev_rat.png',bbox_inches="tight")


# In[116]:


X = df2['Reviews'].values # axis x
Y = df2['Rating'].values # axis y
area = playstore['Installs'].values/10000000 # ukuran besar/kecilnya lingkaran scatter plot
fig = plt.figure(figsize=(5,5))
fig.add_subplot()
# isi nama method untuk scatter plot, variabel x, dan variabel y
plt.scatter(x=X,y=Y, s=area, alpha=0.3)
plt.xlabel('Reviews')
plt.ylabel('Rating')
plt.savefig('rev_rat.png',bbox_inches="tight")


# **Membuat Histogram Size Distribution**

# **_Task 9:_** Buatlah sebuah histogram yang menggambarkan distribusi Size aplikasi dalam satuan Mb(Megabytes). Histogram yang terbentuk terbagi menjadi 100 bins

# In[117]:


#X=(df2['Size'/1000000).values
#fig = plt.figure(figsize=(5,5))
#fig.add_subplot()
#plt.hist(X,bins=100, density=True,  alpha=0.75)
#plt.xlabel('Size')
#plt.ylabel('Frequency')
#plt.savefig('hist_size.png',bbox_inches="tight")


# In[118]:


X=(df2['Size']/1000000).values
fig = plt.figure(figsize=(5,5))
fig.add_subplot()
plt.hist(X,bins=100, density=True,  alpha=0.75)
plt.xlabel('Size')
plt.ylabel('Frequency')
plt.savefig('hist_size.png',bbox_inches="tight")


# **_Task 10:_** Buatlah plot berdasarkan hasil analisis anda. Plot yang dibuat tidak diperbolehkan sama dengan plot yang sudah dicontohkan.

# In[119]:


## code here
pricebox=df2.groupby(by='Category').agg({'Price' : 'mean' }).rename({'Price':'Average_Price'}, axis=1).sort_values(by='Average_Price',ascending=False).head()
pricebox


# In[120]:


pricebox.plot(kind='bar')
#plt.title('Top 5 Category Highest Average Price')
plt.xlabel('Category')
plt.ylabel('Average Price in $')
#plt.colorbar()
plt.savefig('pricebox.png',bbox_inches="tight")


# In[ ]:




