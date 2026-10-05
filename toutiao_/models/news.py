class Category(Base):
    """
    新闻分类表模型
    对应数据库中的 news_category 表。
    """
 
    # 指定数据库表名
    __tablename__ = "news_category"
 
    # 主键ID：
    # primary_key=True 表示主键
    # autoincrement=True 表示自增
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="分类ID"
    )
 
    # 分类名称：
    # unique=True 表示分类名称不能重复
    # nullable=False 表示不能为空
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment="分类名称"
    )
 
    # 排序字段：
    # 数字越小越靠前，默认是 0
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="排序"
    )
 
    # 打印对象时显示更清楚，方便调试
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order})>"
 
class News(Base):
    # 指定数据库表名
    __tablename__ = "news"
 
    # 创建索引：提升查询速度 → 添加目录
    __table_args__ = (
        Index('fk_news_category_idx', 'category_id'),  # 高频查询场景
        Index('idx_publish_time', 'publish_time')  # 按发布时间排序
    )
 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="新闻ID")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻标题")
    description: Mapped[Optional[str]] = mapped_column(String(500), comment="新闻简介")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image: Mapped[Optional[str]] = mapped_column(String(255), comment="封面图片URL")
    author: Mapped[Optional[str]] = mapped_column(String(50), comment="作者")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_category.id'), nullable=False, comment="分类ID")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="发布时间")
 
    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}', views={self.views})>"

async def get_news_detail(
        db: AsyncSession,
        new_id : int
):
    # 获取新闻详情
    stmt = select(News).where(News.id == new_id)
    result = await db.execute(stmt)
 
    return result.scalar_one_or_none()