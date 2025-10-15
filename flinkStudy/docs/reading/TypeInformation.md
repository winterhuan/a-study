# 类型系统

## TypeInformation

TypeInformation is the core class of Flink's type system. Flink requires a type information for
all types that are used as input or return type of a user function. This type information class
acts as the tool to generate serializers and comparators, and to perform semantic checks such as
whether the fields that are used as join/grouping keys actually exist.

TypeInformation 是 Flink 类型系统的核心类。Flink 需要为所有用作用户函数输入或返回类型的类型提供类型信息。这个类型信息类 充当生成序列化器和比较器的工具，并执行语义检查，例如检查用作连接/分组键的字段是否确实存在。

The type information also bridges between the programming languages object model and a logical
flat schema. It maps fields from the types to columns (fields) in a flat schema. Not all fields
from a type are mapped to a separate fields in the flat schema and often, entire types are mapped
to one field. It is important to notice that the schema must hold for all instances of a type.
For that reason, elements in lists and arrays are not assigned to individual fields, but the
lists and arrays are considered to be one field in total, to account for different lengths in the
arrays.

类型信息还在编程语言的对象模型与逻辑平面模式之间架起桥梁。它将类型中的字段映射到平面模式中的列（字段）。并非类型中的所有字段 都被映射到平面模式中的单独字段，通常整个类型被映射到一个字段。重要的是要注意，模式必须对该类型的所有实例都成立。 因此，列表和数组中的元素不会分配到单独的字段，而是将列表和数组整体视为一个字段，以适应数组中不同的长度。

- Basic types are indivisible and are considered a single field.
- Arrays and collections are one field
- Tuples and case classes represent as many fields as the class has fields

基本类型是不可分割的，被视为单个字段。
数组和集合是一个字段
元组和案例类表示与该类具有的字段一样多的字段

To represent this properly, each type has an <i>arity</i> (the number of fields it contains
 directly), and a <i>total number of fields</i> (number of fields in the entire schema of this
 type, including nested types).

 为了正确表示这一点，每种类型都有一个元数（它直接包含的字段数）和一个总字段数（该类型整个模式中的字段数，包括嵌套类型）。

考虑下面的例子：

Consider the example below:

```java
public class InnerType {
public int id;
public String text;
}
public class OuterType {
public long timestamp;
public InnerType nestedType;
}
```

The types "id", "text", and "timestamp" are basic types that take up one field. The
"InnerType" has an arity of two, and also two fields totally. The "OuterType" has an arity of two
fields, and a total number of three fields ( it contains "id", "text", and "timestamp" through
recursive flattening).

"id"、"text"和"timestamp"类型是基本类型，各占一个字段。"InnerType"的元数为2，总字段数也为2。"OuterType"的元数为2个字段， 总字段数为3个（它通过递归展开包含"id"、"text"和"timestamp"）。
