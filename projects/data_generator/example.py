from datetime import datetime, timedelta

from pydantic import Field

from data_generator.generator import DataRecipe, DataFactory
from data_generator.persistence import JsonPersistence
from data_generator.schema import DataSchema
from data_generator.templates import Template, TemplateBuilder


class UserSchema(DataSchema):
    id: int
    temperature: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Create data template
user_template = (
    TemplateBuilder()
    .add_field("id", Template().sequence())
    .add_field("temperature", Template().randnorm(25, 2))
    .add_field("timestamp", Template().date_range(
        datetime.now() - timedelta(days=365),
        datetime.now()
    ))
    .build()
)



class UserRecipe(DataRecipe):
    def __init__(self):
        super().__init__(
            "users",
            schema=UserSchema
        )
        self.template = user_template
        
    def _generate(self, input_data=None):
        return [self.template() for _ in range(100)]

def main():
    # Create factory with MongoDB persistence
    factory = DataFactory()
    
    # Add recipes
    factory.add_recipe(UserRecipe())
    
    # Generate data in parallel
    data = factory.generate()
    
    # Print metrics
    print("Generation Metrics:", factory.get_metrics())
    
    # Cleanup
    factory.cleanup()

if __name__ == "__main__":
    main()