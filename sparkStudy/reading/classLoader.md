# 类加载器

## 类加载器概述

在 JVM 中，类加载器负责将类文件加载到内存中并转换为 JVM 可以使用的 Class 对象。

JVM 有以下几种内置的类加载器：

- Bootstrap ClassLoader - 加载核心 Java 类库（如 rt.jar）
- Extension ClassLoader - 加载扩展类库
- System ClassLoader（也称为 Application ClassLoader）- 加载应用程序类路径中的类
这些类加载器遵循双亲委派模型（Parent Delegation Model），即当一个类加载器收到类加载请求时，它首先委托给父类加载器尝试加载，只有在父类加载器无法加载时才自己尝试加载。

Spark 的自定义类加载器与 JVM 内置类加载器的关系如下：

- 继承关系：Spark 的类加载器都继承自 JVM 的 ClassLoader 类
- 委派模型：除了 ChildFirstURLClassLoader 外，其他类加载器都遵循 JVM 的双亲委派模型
- 上下文类加载器：Spark 经常使用线程上下文类加载器来确保在不同线程中能正确加载类
通过这种方式，Spark 能够灵活地管理类加载，支持用户自定义类、插件和 REPL 环境中的动态类加载需求。

## 类加载器在 Spark 中的应用场景

- 用户 JAR 包加载：支持用户添加的 JAR 包，可以通过 spark.executor.userClassPathFirst 配置决定加载顺序
- REPL 环境：在交互式环境中优先加载用户定义的类
- 动态资源发现：加载用户自定义的资源发现类
- 插件系统：支持 Spark 插件的类加载

## 类加载器的继承关系

- java.lang.ClassLoader - 所有类加载器的基类
- java.net.URLClassLoader - 继承自 ClassLoader，支持从 URL 加载类和资源
- org.apache.spark.util.MutableURLClassLoader - Spark 自定义类加载器，继承自 URLClassLoader，增加了 addURL 方法，允许在运行时动态添加 URL。
- org.apache.spark.util.ChildFirstURLClassLoader - Spark 自定义类加载器，继承自 MutableURLClassLoader，实现了子优先的类加载策略，即优先从自己的 URL 中加载类，而不是先委托给父类加载器。
这种继承关系允许 Spark 灵活地管理类加载，支持动态添加类路径、控制类加载顺序等功能。

### MutableURLClassLoader

MutableURLClassLoader 是 Spark 对标准 URLClassLoader 的扩展，主要增加了 addURL 方法，允许在运行时动态添加新的 URL 到类路径中。

```java
public class MutableURLClassLoader extends URLClassLoader {
    @Override
    public void addURL(URL url) {
        super.addURL(url);
    }
}
```

### ChildFirstURLClassLoader

ChildFirstURLClassLoader 是一种特殊的类加载器，它打破了标准的双亲委派模型，优先从子类加载器（即当前类加载器）加载类，只有当无法加载时才委托给父类加载器。这种设计在以下场景中非常有用：

- 当需要覆盖父类加载器中的类时
- 在 REPL 环境中，用户定义的类需要优先于系统类加载

```java
public class ChildFirstURLClassLoader extends MutableURLClassLoader {
    @Override
    public Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException {
        try {
            return super.loadClass(name, resolve);
        } catch (ClassNotFoundException cnf) {
            return parent.loadClass(name, resolve);
        }
    }
}
```
