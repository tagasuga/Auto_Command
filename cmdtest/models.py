from django.db import models

# Create your models here.

class Cmdcase(models.Model):
    Product = models.ForeignKey('product.Product',on_delete=models.CASCADE,null=True)        # 关联产品id
    cmdcasename = models.CharField('用例名称',max_length=200)       # 测试用例名称
    cmdtestresult = models.BooleanField('测试结果')                 # 测试结果
    cmdtester = models.CharField('测试负责人',max_length=16)        # 执行人
    create_time = models.DateTimeField('创建时间',auto_now=True)    # 创建时间-自动获取当前时间
    class Meta:
        verbose_name = 'cmd测试用例'
        verbose_name_plural = 'cmd测试用例'
    def __str__(self):
        return self.cmdcasename

class Cmdcasestep(models.Model):
    Cmdcase = models.ForeignKey('Cmdcase',on_delete=models.CASCADE)    # 关联接口id
    cmdteststep = models.CharField('测试步聚',max_length=200)        # 测试步聚
    cmdtestobjname = models.CharField('cmd命令',max_length=200) # 测试对象名称描述
    assertdeclare = models.CharField('断言种类',max_length=200)      # 定位方式
    assertInfo1 = models.CharField('断言命令1',max_length=200)       # 控件元素
    assertInfo2 = models.CharField('断言命令2',max_length=200,null=True,blank=True)       # 操作方法
    assertInfo3 = models.CharField('断言命令3',max_length=200,null=True,blank=True)
    assertInfo4 = models.CharField('断言命令4',max_length=200,null=True,blank=True)
    cmdtestdata = models.CharField('测试数据',max_length=200,null=True,blank=True)   # 验证数据
    cmdtestresult = models.BooleanField('测试结果')                  # 测试结果
    create_time = models.DateTimeField('创建时间',auto_now=True)     # 创建时间-自动获取当前时间

    def __str__(self):
        return self.cmdteststep